from collections.abc import Iterable

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from django.contrib.auth.models import AnonymousUser
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
from users.utils.consts import UUID_REGEX

from .models import Appointment, Research, Participation, EncryptedToken
from .permissions import *
from .serializers import (
    AppointmentSerializer,
    ResearchUserSerializer,
    ResearchAdminSerializer,
    ParticipationSerializer,
)


class ResearchUserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Research.objects.get_queryset().order_by("-created")
    serializer_class = ResearchUserSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


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
            for data in request.data:
                if data['research'] != str(research.uuid):
                    raise exceptions.PermissionDenied()
                data['research'] = research.id

                if 'utc-offset' in data:
                    data['when'] = data['when'] + data.pop('utc-offset')

                if appointment_id := data.pop('id', None):
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

    def create(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            raise exceptions.NotAuthenticated()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = Participant.objects.get(pk=request.user.pk).token
        except Participant.DoesNotExist:
            raise exceptions.NotFound("user is not a participant")

        appointment: Appointment = serializer.validated_data["appointment"]
        pubkeys = appointment.get_pubkeys(request.user)

        encrypted_token = EncryptedToken.new(token, pubkeys)
        encrypted_token.save()

        participation = Participation(appointment=appointment, encrypted_token=encrypted_token)
        participation.save()

        return Response(status=status.HTTP_200_OK)

    def get_participations_for_key(self, private_key: RsaKey, participations: Iterable[Participation], request):
        result = []
        for p in participations:
            if token := p.encrypted_token.decrypt(private_key):
                data = self.get_serializer(p, context={"request": request}).data | {"token": token}
                result.append(data)
        return result

    def get_user_participations(self, request: Request) -> Response:
        serializer = PasswordSerializer(data=request.data)
        # serializer = PasswordSerializer(data={"current_password": "asdf"})  # for testing
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["current_password"]
        if not request.user.check_password(password):
            raise exceptions.AuthenticationFailed("invalid password")

        participations = Participation.objects.all()
        _, encrypted_key = request.user.get_keypair()
        private_key = RSA.import_key(encrypted_key, password)

        return Response(self.get_participations_for_key(private_key, participations, request))

    def get_research_participations(self, request: Request, research_id: int) -> Response:
        research: Research = get_object_or_404(Research, pk=research_id)
        _, encrypted_key = research.get_keypair()
        private_key = RSA.import_key(encrypted_key, "unprotected")

        participations = Participation.objects.filter(appointment__research=research)
        return Response(self.get_participations_for_key(private_key, participations, request))

    @action(detail=False, name="Get decrypted", methods=[HTTPMethod.GET])
    def get_decrypted_participations(self, request: Request):
        research_id = request.GET.get("research", default=None)
        if research_id:
            return self.get_research_participations(request, research_id)
        if not isinstance(request.user, AnonymousUser):
            return self.get_user_participations(request)
        raise exceptions.ParseError("missing research query parameter")
