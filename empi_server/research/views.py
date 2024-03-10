from collections.abc import Iterable
from http import HTTPMethod

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, mixins, status, exceptions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from users.models import Participant
from users.serializers import PasswordSerializer

from .models import Appointment, Research, Participation, EncryptedToken
from .serializers import (
    AppointmentSerializer,
    ResearchSerializer,
    ParticipationSerializer,
)


class ResearchViewSet(viewsets.ModelViewSet):
    queryset = Research.objects.get_queryset().order_by("-created")
    serializer_class = ResearchSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.get_queryset().order_by("pk")
    serializer_class = AppointmentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data + {"type": instance.get_type()})


class ParticipationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Participation.objects.get_queryset().order_by("pk")
    serializer_class = ParticipationSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            raise exceptions.NotAuthenticated()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = Participant.objects.get(pk=request.user.pk).token
        except Participant.DoesNotExist:
            raise exceptions.NotFound("user is not a participant")

        try:
            appointment: Appointment = serializer.validated_data["appointment"]
        except Appointment.DoesNotExist:
            raise exceptions.ParseError("the specified appointment was not found")
        pubkeys = appointment.get_pubkeys(request.user)

        encrypted_token = EncryptedToken.new(token, pubkeys)
        encrypted_token.save()

        participation = Participation(
            appointment=appointment, encrypted_token=encrypted_token
        )
        participation.save()

        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def get_participations_for_key(
        private_key: RsaKey, participations: Iterable[Participation], request
    ):
        result = []
        for p in participations:
            if token := p.encrypted_token.decrypt(private_key):
                data = ParticipationSerializer(p, context={"request": request}).data | {
                    "token": token
                }
                result.append(data)
        return result

    @staticmethod
    def get_user_participations(request: Request) -> Response:
        # serializer = PasswordSerializer(data=request.data)
        serializer = PasswordSerializer(
            data={"current_password": "asdf"}
        )  # for testing
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["current_password"]
        if not request.user.check_password(password):
            raise exceptions.AuthenticationFailed("invalid password")

        participations = Participation.objects.all()
        _, encrypted_key = request.user.get_keypair()
        private_key = RSA.import_key(encrypted_key, password)

        return Response(
            ParticipationViewSet.get_participations_for_key(
                private_key, participations, request
            )
        )

    @staticmethod
    def get_research_participations(request: Request) -> Response:
        try:
            research: Research = Research.objects.get(pk=request.GET["research"])
            _, encrypted_key = research.get_keypair()
            private_key = RSA.import_key(encrypted_key, "unprotected")

            participations = Participation.objects.filter(
                appointment__research=research
            )
            return Response(
                ParticipationViewSet.get_participations_for_key(
                    private_key, participations, request
                )
            )
        except Research.DoesNotExist:
            raise exceptions.NotFound("the specified research does not exist")

    @action(detail=False, name="Get decrypted", methods=[HTTPMethod.GET])
    def get_decrypted_participations(self, request: Request):
        research_id = request.GET.get("research", default=None)
        if research_id:
            return self.get_research_participations(request)
        if not isinstance(request.user, AnonymousUser):
            return self.get_user_participations(request)
        raise exceptions.ParseError("missing research query parameter")
