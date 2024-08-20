from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.routers import reverse
from rest_framework.status import HTTP_200_OK

from emails.types import PasswordResetEmail
from research.models import Research
from .models import EmpiUser, Participant, Attribute, AttributeValue, ResetKey
from .permissions import *
from .serializers import (
    UserSerializer,
    PasswordSerializer,
    ParticipantSerializer,
    AttributeSerializer,
    PasswordResetSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = EmpiUser.users.get_queryset().filter(is_active=True).order_by("date_joined")
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
        if request.user != self.get_object():
            raise exceptions.AuthenticationFailed("only changing own password is allowed")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]
        if not user.check_password(current_password):
            raise exceptions.AuthenticationFailed("invalid current password")
        user.change_password(current_password, new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        name="Change password by admin",
        methods=[HTTPMethod.POST],
        serializer_class=PasswordSerializer,
        permission_classes=[IsAdminUser],
    )
    def change_password_admin(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: EmpiUser = self.get_object()
        admin: EmpiUser = request.user

        admin_password = serializer.validated_data["current_password"]
        new_user_password = serializer.validated_data["new_password"]

        user.change_password_admin(admin, admin_password, new_user_password)

        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True, methods=[HTTPMethod.POST], serializer_class=PasswordSerializer, permission_classes=[IsAdminUser]
    )
    def start_password_reset(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: EmpiUser = self.get_object()
        admin: EmpiUser = request.user

        admin_password = serializer.validated_data["current_password"]
        passphrase = user.make_reset_key(admin, admin_password)

        email = PasswordResetEmail(passphrase, [user.email])
        email.send()

        return Response(status=HTTP_200_OK)

    @action(
        detail=True, methods=[HTTPMethod.POST], serializer_class=PasswordResetSerializer, permission_classes=[AllowAny]
    )
    def complete_password_reset(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: EmpiUser = self.get_object()
        passphrase = serializer.validated_data["passphrase"]
        new_password = serializer.validated_data["new_password"]

        reset_key = get_object_or_404(ResetKey, user=user.pk)
        if timezone.now() > reset_key.valid_until:
            reset_key.delete()
            _ = get_object_or_404(ResetKey, user=user.pk)

        user.reset_password(reset_key, passphrase, new_password)

    @action(
        detail=False,
        name="Check password",
        methods=[HTTPMethod.POST],
        serializer_class=PasswordSerializer,
        permission_classes=[IsAuthenticated],
    )
    def check_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: EmpiUser = request.user
        if user.check_password(request.data["current_password"]):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, name="Get own details", methods=[HTTPMethod.GET], permission_classes=[IsAuthenticated])
    def get_self(self, request):
        user: EmpiUser = request.user
        serializer = self.get_serializer(instance=user, context={"request": request})
        return HttpResponseRedirect(reverse("empiuser-detail", [serializer.data["id"]], request=request))


class ParticipantViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Participant.objects.get_queryset().filter(user__is_active=True).order_by("pk")
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
        participant = get_object_or_404(Participant, pk=pk)
        if request.method == HTTPMethod.POST:
            for name, values in request.data.items():
                new_chosen_values = AttributeValue.objects.filter(attribute__name=name).filter(value__in=values)
                to_keep = participant.chosen_attribute_values.filter(~Q(attribute__name=name))
                participant.chosen_attribute_values.set(to_keep.union(new_chosen_values))
            participant.save()
        return Response(AttributeValue.group_by_attribute(participant.chosen_attribute_values.all()))

    @action(
        detail=False,
        name="Attributes for research",
        methods=[HTTPMethod.GET, HTTPMethod.POST],
        url_path="research/(?P<nanoid>[A-Z0-9-]{20}/?)",
        permission_classes=[AllowAny],
    )
    def research(self, request, nanoid=None):
        research = get_object_or_404(Research, nanoid=nanoid)
        if request.method == HTTPMethod.POST:
            for name, values in request.data.items():
                new_chosen_values = AttributeValue.objects.filter(attribute__name=name).filter(value__in=values)
                to_keep = research.chosen_attribute_values.filter(~Q(attribute__name=name))
                research.chosen_attribute_values.set(to_keep.union(new_chosen_values))
            research.save()
        return Response(AttributeValue.group_by_attribute(research.chosen_attribute_values.all()))
