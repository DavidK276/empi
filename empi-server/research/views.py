from collections.abc import Iterable

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import *
from rest_framework.request import Request
from rest_framework.response import Response

from emails.types import PublicSignupEmail, ResearchCreatedEmail, NewSignupEmail, CancelSignupEmail
from users.models import Participant
from users.serializers import PasswordSerializer
from .auth import ResearchAuthentication
from .models import Appointment, Research, Participation, EncryptedToken
from .permissions import *
from .serializers import (
    AppointmentSerializer,
    ResearchUserSerializer,
    ResearchAdminSerializer,
    ParticipationSerializer,
    ParticipationUpdateSerializer,
    AnonymousParticipationSerializer,
)


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


class ResearchAdminViewSet(viewsets.ModelViewSet):
    queryset = Research.objects.get_queryset().order_by("-created")
    serializer_class = ResearchAdminSerializer
    authentication_classes = [ResearchAuthentication, TokenAuthentication, SessionAuthentication]
    permission_classes = [ResearchPermission]
    lookup_field = "nanoid"

    def create(self, request, *args, **kwargs):
        serializer: ResearchAdminSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            research = serializer.save()
            email = ResearchCreatedEmail(research)
            email.send()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(
        detail=True,
        name="Change password",
        methods=[HTTPMethod.POST],
        serializer_class=PasswordSerializer,
        url_path="password/set",
    )
    def change_password(self, request, nanoid=None):
        research: Research = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]
        research.change_password(current_password, new_password)
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        name="Check password",
        methods=[HTTPMethod.POST],
        permission_classes=[AllowAny],
        serializer_class=PasswordSerializer,
        url_path="password/check",
    )
    def check_password(self, request, nanoid=None):
        research: Research = self.get_object()
        if research.is_protected:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            _, encrypted_key = research.get_keypair()
            current_password = serializer.validated_data["current_password"]
            try:
                _ = RSA.import_key(encrypted_key, current_password)
            except (ValueError, IndexError, TypeError):
                raise exceptions.PermissionDenied("invalid current password")
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=[HTTPMethod.GET, HTTPMethod.PUT],
        serializer_class=AppointmentSerializer,
    )
    @transaction.atomic
    def appointments(self, request, nanoid=None):
        research: Research = self.get_object()

        if request.method == HTTPMethod.PUT:
            to_keep = []
            if not isinstance(request.data, list):
                data_list: list[dict[str]] = [request.data]
            else:
                data_list = request.data
            for data in data_list:
                data["research"] = research.id

                if appointment_id := data.pop("id", None):
                    appointment = get_object_or_404(Appointment, pk=appointment_id)
                    serializer: AppointmentSerializer = self.get_serializer(appointment, data=data)
                else:
                    serializer: AppointmentSerializer = self.get_serializer(data=data)

                serializer.is_valid(raise_exception=True)
                appointment: Appointment = serializer.save()
                to_keep.append(appointment.pk)

            Appointment.objects.filter(~Q(pk__in=to_keep) & Q(research=research)).delete()

        appointments = Appointment.objects.filter(research=research)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)


class ParticipationViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Participation.objects.get_queryset().filter(encrypted_token__isnull=False)
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participant = get_object_or_404(Participant, pk=request.user.pk)

        appointment: Appointment = serializer.validated_data["appointment"]
        if appointment.free_capacity <= 0:
            raise exceptions.ParseError("no free capacity left for this appointment")
        pubkeys = appointment.get_pubkeys(request.user)

        with transaction.atomic():
            encrypted_token = EncryptedToken.new(participant.token, pubkeys)
            encrypted_token.save()

            participation = Participation(appointment=appointment, encrypted_token=encrypted_token)
            participation.save()

            email = NewSignupEmail(appointment)
            email.send()

        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_user_token = get_object_or_404(Participant, pk=request.user.pk).token
        participation: Participation = self.get_object()

        _, encrypted_key = request.user.get_keypair()
        private_key = RSA.import_key(encrypted_key, serializer.validated_data["current_password"])
        if participation_token := participation.encrypted_token.decrypt(private_key):
            if participation_token == request_user_token:
                email = CancelSignupEmail(participation.appointment)
                email.send()

                return super().destroy(request, *args, **kwargs)

        raise exceptions.PermissionDenied()

    @staticmethod
    def get_participations_for_key(private_key: RsaKey, participations: Iterable[Participation], request):
        result = []
        for p in participations:
            if token := p.encrypted_token.decrypt(private_key):
                data = ParticipationSerializer(p, context={"request": request}).data
                data |= {"token": token}
                data |= {"research": p.appointment.research.pk}
                result.append(data)
        return result

    @action(detail=False, methods=[HTTPMethod.POST], serializer_class=PasswordSerializer, url_path="user")
    def user_participations(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["current_password"]
        if not request.user.check_password(password):
            raise exceptions.AuthenticationFailed("invalid password")

        participations = self.get_queryset()
        _, encrypted_key = request.user.get_keypair()
        private_key = RSA.import_key(encrypted_key, password)

        return Response(self.get_participations_for_key(private_key, participations, request))

    @action(
        detail=False,
        methods=[HTTPMethod.POST],
        permission_classes=[AllowAny],
        url_path="research/(?P<nanoid>[A-Z0-9-]{20})/(?P<action>get|set/?)",
    )
    def research_participations(self, request: Request, nanoid: str, action: str) -> Response:
        research: Research = get_object_or_404(Research, nanoid=nanoid)

        if action == "get":
            if research.is_protected:
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
            participations = self.get_queryset()
            return Response(self.get_participations_for_key(private_key, participations, request))

        serializer = ParticipationUpdateSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        data = {data["id"]: data["is_confirmed"] for data in serializer.data}
        participations = Participation.objects.filter(appointment__research=research).filter(pk__in=data.keys())
        for participation in participations:
            participation.is_confirmed = data[participation.pk]
            participation.save()
        return Response(status.HTTP_200_OK)


class AnonymousParticipationViewSet(viewsets.ModelViewSet):
    queryset = Participation.objects.get_queryset().filter(encrypted_token__isnull=True)
    serializer_class = AnonymousParticipationSerializer
    permission_classes = [AllowAllExceptList | IsAdminUser]
    lookup_field = "nanoid"

    def create(self, request, *args, **kwargs):
        serializer: AnonymousParticipationSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointment: Appointment = serializer.validated_data["appointment"]
        if appointment.free_capacity <= 0:
            raise exceptions.ParseError("no free capacity left for this appointment")

        with transaction.atomic():
            participation = serializer.save()
            email = PublicSignupEmail(participation.nanoid, [serializer.validated_data["recipient"]])
            email.send()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
