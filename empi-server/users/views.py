from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponseRedirect
from research.models import Research
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import *
from rest_framework.response import Response

from .models import EmpiUser, Participant, Attribute, AttributeValue
from .permissions import *
from .serializers import (
    UserSerializer,
    PasswordSerializer,
    ParticipantSerializer,
    AttributeSerializer,
)
from empi_server.constants import UUID_REGEX


class UserViewSet(viewsets.ModelViewSet):
    queryset = EmpiUser.users.get_queryset().order_by("date_joined")
    serializer_class = UserSerializer
    permission_classes = [(IsAuthenticatedOrReadOnly & IsSelf) | IsAdminUser]

    @action(
        detail=True,
        name="Change password",
        methods=[HTTPMethod.POST],
        serializer_class=PasswordSerializer,
    )
    def change_password(self, request, pk=None):
        user: EmpiUser = self.get_object()
        if isinstance(request.user, AnonymousUser) or request.user != self.get_object():
            raise exceptions.AuthenticationFailed("only changing own password is allowed")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]
        if not user.check_password(current_password):
            raise exceptions.NotFound("invalid current password")
        user.change_password(current_password, new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, name="Check password", methods=[HTTPMethod.POST], serializer_class=PasswordSerializer)
    def check_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if isinstance(request.user, AnonymousUser):
            return exceptions.NotAuthenticated()
        user: EmpiUser = request.user
        if user.check_password(request.data["current_password"]):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, name="Get own details", methods=[HTTPMethod.GET], permission_classes=[IsAuthenticated])
    def get_self(self, request):
        user: EmpiUser = request.user
        serializer = self.get_serializer(instance=user, context={"request": request})
        return HttpResponseRedirect(serializer.data["url"])


class ParticipantViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Participant.objects.get_queryset().order_by("pk")
    serializer_class = ParticipantSerializer
    permission_classes = [ReadOnly | IsAdminUser]

    @action(
        detail=False,
        name="Register",
        methods=[HTTPMethod.POST],
        permission_classes=[AllowAny],
        serializer_class=UserSerializer,
    )
    def register(self, request):
        serializer: UserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: EmpiUser = serializer.save()
        participant = Participant(user=user)
        participant.save()
        participant_serializer = ParticipantSerializer(instance=participant, context={"request": request})
        return Response(participant_serializer.data, status=status.HTTP_201_CREATED)


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.get_queryset().order_by("pk")
    serializer_class = AttributeSerializer
    permission_classes = [IsSelf | ReadOnly | IsAdminUser]

    @action(
        detail=False,
        name="Attributes for participant",
        methods=[HTTPMethod.GET, HTTPMethod.POST],
        url_path="participant/(?P<pk>[0-9]+/?)",
    )
    def participant(self, request, pk=None):
        try:
            participant: Participant = Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            raise exceptions.NotFound("participant does not exist")
        if request.method == HTTPMethod.POST:
            for name, values in request.data.items():
                new_chosen_values = AttributeValue.objects.filter(attribute__name=name).filter(value__in=values)
                to_keep = participant.chosen_attribute_values.filter(~Q(attribute__name=name))
                participant.chosen_attribute_values.set(to_keep.union(new_chosen_values))
            participant.save()
        return Response(AttributeValue.group_by_attribute(participant.chosen_attribute_values.all()))

    @action(
        detail=False,
        name="Attributes for current user",
        methods=[HTTPMethod.GET, HTTPMethod.POST],
        url_path="participant",
        permission_classes=[IsAuthenticated],
    )
    def get_self(self, request):
        pk = request.user.pk
        return self.participant(request, pk)

    @action(
        detail=False,
        name="Attributes for research",
        methods=[HTTPMethod.GET, HTTPMethod.POST],
        url_path=f"research/(?P<uuid>{UUID_REGEX}/?)",
        permission_classes=[AllowAny],
    )
    def research(self, request, uuid=None):
        try:
            research: Research = Research.objects.get(uuid=uuid)
        except Research.DoesNotExist:
            raise exceptions.NotFound("research does not exist")
        if request.method == HTTPMethod.POST:
            for name, values in request.data.items():
                new_chosen_values = AttributeValue.objects.filter(attribute__name=name).filter(value__in=values)
                to_keep = research.chosen_attribute_values.filter(~Q(attribute__name=name))
                research.chosen_attribute_values.set(to_keep.union(new_chosen_values))
            research.save()
        return Response(AttributeValue.group_by_attribute(research.chosen_attribute_values.all()))
