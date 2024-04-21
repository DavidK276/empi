from collections.abc import Iterable

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import *
from rest_framework.request import Request
from rest_framework.response import Response
from users.models import Participant
from users.serializers import PasswordSerializer

from .models import Appointment, Research, Participation, EncryptedToken
from .permissions import *
from .serializers import (
    AppointmentSerializer,
    ResearchUserSerializer,
    ResearchAdminSerializer,
    ParticipationSerializer, ParticipationUpdateSerializer,
)
from empi_server.constants import UUID_REGEX


class ResearchUserViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Research.objects.get_queryset().filter(is_published=True).order_by("-created")
    serializer_class = ResearchUserSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    @action(
        detail=True,
        methods=[HTTPMethod.GET],
        serializer_class=AppointmentSerializer,
    )
    @transaction.atomic
    def appointments(self, request, id=None):
        research: Research = self.get_object()

        appointments = Appointment.objects.filter(research=research)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ResearchAdminViewSet(viewsets.ModelViewSet):
    queryset = Research.objects.get_queryset().order_by("-created")
    serializer_class = ResearchAdminSerializer
    permission_classes = [AllowAllExceptList | IsAdminUser]
    lookup_field = "uuid"

    @action(
        detail=True,
        name="Change password",
        methods=[HTTPMethod.PUT],
        serializer_class=PasswordSerializer,
    )
    def change_password(self, request, uuid=None):
        research: Research = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]
        research.change_password(current_password, new_password)
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=[HTTPMethod.GET, HTTPMethod.PUT],
        serializer_class=AppointmentSerializer,
    )
    @transaction.atomic
    def appointments(self, request, uuid=None):
        research: Research = self.get_object()

        if request.method == HTTPMethod.PUT:
            to_keep = []
            if not isinstance(request.data, list):
                data_list: list[dict[str]] = [request.data]
            else:
                data_list = request.data
            for data in data_list:
                data["research"] = research.id
                if "utc-offset" in data:
                    data["when"] = data["when"] + data.pop("utc-offset")

                if appointment_id := data.pop("id", None):
                    appointment = get_object_or_404(Appointment, pk=appointment_id)
                    serializer: AppointmentSerializer = self.get_serializer(appointment, data=data)
                else:
                    serializer: AppointmentSerializer = self.get_serializer(data=data)

                serializer.is_valid(raise_exception=True)
                appointment: Appointment = serializer.save()
                to_keep.append(appointment.pk)

            Appointment.objects.filter(~Q(pk__in=to_keep)).delete()

        appointments = Appointment.objects.filter(research=research)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)


class ParticipationViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Participation.objects.get_queryset().order_by("pk")
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = get_object_or_404(Participant, pk=request.user.pk).token

        appointment: Appointment = serializer.validated_data["appointment"]
        pubkeys = appointment.get_pubkeys(request.user)

        encrypted_token = EncryptedToken.new(token, pubkeys)
        encrypted_token.save()

        participation = Participation(appointment=appointment, encrypted_token=encrypted_token)
        participation.save()

        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def get_participations_for_key(private_key: RsaKey, participations: Iterable[Participation], request):
        result = []
        for p in participations:
            if token := p.encrypted_token.decrypt(private_key):
                data = ParticipationSerializer(p, context={"request": request}).data | {"token": token}
                result.append(data)
        return result

    @action(
        detail=False,
        methods=[HTTPMethod.POST],
        serializer_class=PasswordSerializer,
        url_path="user"
    )
    def user_participations(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["current_password"]
        if not request.user.check_password(password):
            raise exceptions.AuthenticationFailed("invalid password")

        participations = Participation.objects.all()
        _, encrypted_key = request.user.get_keypair()
        private_key = RSA.import_key(encrypted_key, password)

        return Response(self.get_participations_for_key(private_key, participations, request))

    @action(
        detail=False,
        methods=[HTTPMethod.POST],
        permission_classes=[AllowAny],
        url_path=f"research/(?P<uuid>{UUID_REGEX})/(?P<action>get|set/?)",
    )
    def research_participations(self, request: Request, uuid: str, action: str) -> Response:
        research: Research = get_object_or_404(Research, uuid=uuid)

        if action == 'get':
            if research.protected:
                serializer = PasswordSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                password = serializer.validated_data["current_password"]
            else:
                password = "unprotected"
            _, encrypted_key = research.get_keypair()
            try:
                private_key = RSA.import_key(encrypted_key, password)
            except (ValueError, IndexError, TypeError):
                raise exceptions.AuthenticationFailed("invalid password")
            participations = Participation.objects.filter(appointment__research=research)
            return Response(self.get_participations_for_key(private_key, participations, request))

        serializer = ParticipationUpdateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data = {data["id"]: data["has_participated"] for data in serializer.data}
        participations = Participation.objects.filter(appointment__research=research).filter(pk__in=data.keys())
        for participation in participations:
            participation.has_participated = data[participation.pk]
            participation.save()
        return Response(status.HTTP_200_OK)
