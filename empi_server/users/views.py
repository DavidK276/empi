from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import *

from .models import EmpiUser, Participant, Attribute, AttributeValue
from .serializers import (
    UserSerializer,
    PasswordSerializer,
    ParticipantSerializer,
    AttributeSerializer,
)

from research.models import Research
from .permissions import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = EmpiUser.objects.get_queryset().order_by("date_joined")
    serializer_class = UserSerializer
    permission_classes = [CreateOnly | (IsAuthenticatedOrReadOnly & IsSelf) | IsAdminUser]

    @action(
        detail=True,
        name="Change password",
        methods=[HTTPMethod.POST],
        serializer_class=PasswordSerializer,
    )
    def change_password(self, request, pk=None):
        user: EmpiUser = self.get_object()
        if isinstance(request.user, AnonymousUser) or request.user == self.get_object():
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


class ParticipantViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Participant.objects.get_queryset().order_by("pk")
    serializer_class = ParticipantSerializer
    permission_classes = [CreateOnly | ReadOnly | IsAdminUser]


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.get_queryset().order_by("pk")
    serializer_class = AttributeSerializer
    permission_classes = [ReadOnly | IsAdminUser]

    @action(
        detail=False,
        name="Get attributes for user",
        methods=[HTTPMethod.GET, HTTPMethod.POST],
        url_path="participant/(?P<participant_pk>[0-9]+/?)",
    )
    def participant(self, request, participant_pk=None):
        try:
            participant: Participant = Participant.objects.get(pk=participant_pk)
        except Participant.DoesNotExist:
            raise exceptions.NotFound("participant does not exist")
        if request.method == HTTPMethod.POST:
            for name, values in request.data.items():
                new_chosen_values = AttributeValue.objects.filter(attribute__name=name).filter(value__in=values)
                participant.chosen_attribute_values.set(new_chosen_values)
            participant.save()
        return Response(AttributeValue.group_by_attribute(participant.chosen_attribute_values.all()))

    @action(
        detail=False,
        name="Attributes for research",
        methods=[HTTPMethod.GET, HTTPMethod.POST],
        url_path="research/(?P<research_pk>[0-9]+/?)",
    )
    def research(self, request, research_pk=None):
        try:
            research: Research = Research.objects.get(pk=research_pk)
        except Research.DoesNotExist:
            raise exceptions.NotFound("research does not exist")
        if request.method == HTTPMethod.POST:
            for name, values in request.data.items():
                new_chosen_values = AttributeValue.objects.filter(attribute__name=name).filter(value__in=values)
                research.chosen_attribute_values.set(new_chosen_values)
            research.save()
        return Response(AttributeValue.group_by_attribute(research.chosen_attribute_values.all()))
