from collections.abc import Iterable

from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as t
from drf_spectacular.utils import extend_schema, OpenApiParameter
from knox.auth import TokenAuthentication
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import *
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from emails.types import PublicSignupEmail, ResearchCreatedEmail, NewSignupEmail, CancelSignupEmail
from users.models import Participant
from users.serializers import PasswordChangeSerializer, PasswordSerializer, ParticipantSerializer
from .models import Appointment, Research, Participation
from .permissions import *
from .serializers import (
    AppointmentSerializer,
    ResearchUserSerializer,
    ResearchAdminSerializer,
    ParticipationSerializer,
    ParticipationUpdateSerializer,
    AnonymousParticipationSerializer,
    ParticipationCreateSerializer,
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
    def appointments(self, request, id=None):  # noqa: F841 the id parameter is needed by DRF
        research: Research = self.get_object()

        appointments = research.appointment_set.order_by("when")
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)


class ResearchAdminViewSet(viewsets.ModelViewSet):
    queryset = Research.objects.get_queryset().order_by("-created")
    serializer_class = ResearchAdminSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
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
        serializer_class=PasswordChangeSerializer,
        url_path="password/set",
    )
    def change_password(self, request, nanoid=None):  # noqa: F841 the nanoid parameter is needed by DRF
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
    def check_password(self, request, nanoid=None):  # noqa: F841 the nanoid parameter is needed by DRF
        research: Research = self.get_object()
        if research.is_protected:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            _, encrypted_key = research.get_keypair()
            current_password = serializer.validated_data["password"]
            try:
                _ = RSA.import_key(encrypted_key, current_password)
            except (ValueError, IndexError, TypeError):
                raise exceptions.PermissionDenied(t("invalid current password"))
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=[HTTPMethod.GET, HTTPMethod.PUT],
        serializer_class=AppointmentSerializer,
    )
    @transaction.atomic
    def appointments(self, request, nanoid=None):  # noqa: F841 the nanoid parameter is needed by DRF
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

            research.appointment_set.filter(~Q(pk__in=to_keep)).delete()

        serializer = self.get_serializer(research.appointment_set, many=True)
        return Response(serializer.data)


class ParticipationViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Used for working with :class:`Participation` objects by registered users.
    """

    queryset = Participation.objects.get_queryset().filter(encrypted_tokens__isnull=False)
    serializer_class = ParticipationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        year = self.request.query_params.get("year")
        if year is not None:
            queryset = queryset.filter(academic_year=year)

        semester = self.request.query_params.get("semester")
        semester = (semester or "").upper()
        if len(semester) > 0 and semester != "ANY":
            queryset = queryset.filter(semester=semester)

        return queryset

    def create(self, request: Request, *args, **kwargs):
        """
        Creates the :class:`Participation` if there is free space in the specified appointment.
        Also sends an info email to the specified address.
        The `is_confirmed` body parameter should not be sent as it is ignored.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participant = get_object_or_404(Participant, pk=request.user.pk)
        appointment: Appointment = serializer.validated_data["appointment"]
        if appointment.free_capacity <= 0:
            raise exceptions.ParseError("no free capacity left for this appointment")

        with transaction.atomic():
            pubkeys = research.get_pubkeys(request.user)
            participation = Participation.new(participant.token, appointment, is_confirmed=False, pubkeys=pubkeys)
            participation.save()

            email = NewSignupEmail(appointment, research)
            email.send()

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=[HTTPMethod.POST], serializer_class=ParticipationCreateSerializer)
    def signup(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        interesting_participations = self.get_queryset().filter(appointment=serializer.validated_data["appointment"])

        _, encrypted_privkey = request.user.get_keypair()
        private_key = RSA.import_key(encrypted_privkey, passphrase=serializer.validated_data["password"])
        for p in interesting_participations:
            if p.decrypt(private_key) is not None:
                return Response(status=HTTP_400_BAD_REQUEST)
        return self.create(request)

    @extend_schema(parameters=[OpenApiParameter("password", str)])
    def destroy(self, request: Request, *args, **kwargs):
        password = request.query_params["password"]
        if not password:
            raise exceptions.ValidationError(t("A password is required"))

        request_user_token = request.user.participant.token
        participation: Participation = self.get_object()

        _, encrypted_key = request.user.get_keypair()
        private_key = RSA.import_key(encrypted_key, password)
        if participation_token := participation.decrypt(private_key):
            if participation_token == request_user_token:
                email = CancelSignupEmail(participation.appointment)
                email.send()

                return super().destroy(request, *args, **kwargs)

        raise exceptions.PermissionDenied()

    @staticmethod
    def get_participations_for_key(private_key: RsaKey, participations: Iterable[Participation], request):
        result = []
        for p in participations:
            if token := p.decrypt(private_key):
                data = ParticipationSerializer(p, context={"request": request}).data
                data |= {"participant": ParticipantSerializer(instance=Participant.objects.get(token=token)).data}
                data |= {
                    "research": ResearchUserSerializer(
                        instance=Research.objects.get(
                            pk=p.appointment.research.pk if p.appointment is not None else p.research.pk
                        )
                    ).data
                }
                result.append(data)
        return result

    @action(detail=False, methods=[HTTPMethod.POST], serializer_class=PasswordSerializer, url_path="user")
    def user_participations(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["password"]
        if not request.user.check_password(password):
            raise exceptions.AuthenticationFailed("invalid password")

        participations = self.get_queryset()
        _, encrypted_key = request.user.get_keypair()
        private_key = RSA.import_key(encrypted_key, password)

        return Response(self.get_participations_for_key(private_key, participations, request))

    @action(
        detail=False,
        methods=[HTTPMethod.POST],
        permission_classes=[],
        serializer_class=PasswordSerializer,
        url_path="research/(?P<nanoid>[A-Z0-9-]{20})/get",
    )
    def get_research_participations(self, request: Request, nanoid: str) -> Response:
        research: Research = get_object_or_404(Research, nanoid=nanoid)

        if research.is_protected:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            password = serializer.validated_data["password"]
        else:
            password = "unprotected"
        _, encrypted_key = research.get_keypair()
        try:
            private_key = RSA.import_key(encrypted_key, password)
        except (ValueError, IndexError, TypeError):
            raise exceptions.AuthenticationFailed("invalid password")
        participations = self.get_queryset()
        return Response(self.get_participations_for_key(private_key, participations, request))

    @action(
        detail=False,
        methods=[HTTPMethod.PUT],
        permission_classes=[],
        serializer_class=ParticipationUpdateSerializer,
        url_path="research/(?P<nanoid>[A-Z0-9-]{20})/set",
    )
    def set_research_participations(self, request: Request, nanoid: str) -> Response:
        research: Research = get_object_or_404(Research, nanoid=nanoid)

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        data = {data["id"]: data["is_confirmed"] for data in serializer.data}
        participations = research.participation_set.filter(pk__in=data.keys())
        for participation in participations:
            participation.is_confirmed = data[participation.pk]
            participation.save(update_fields=["is_confirmed"])
        return Response(status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=[HTTPMethod.GET], permission_classes=[AllowAny])
    def academic_year_choices(self, request: Request) -> Response:
        academic_years = list(self.get_queryset().values_list("academic_year").distinct())
        return Response(data=[x[0] for x in academic_years])


class AnonymousParticipationViewSet(viewsets.ModelViewSet):
    """
    Used for working with :class:`Participation` objects by anonymous users.
    """

    queryset = Participation.objects.get_queryset().filter(encrypted_tokens__isnull=True)
    serializer_class = AnonymousParticipationSerializer
    permission_classes = [AllowAllExceptList | IsAdminUser]
    lookup_field = "nanoid"

    def create(self, request, *args, **kwargs):
        """
        Creates the anonymous :class:`Participation` if there is free space in the specified appointment.
        Also sends an info email to the specified address.
        """
        serializer: AnonymousParticipationSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointment: Appointment = serializer.validated_data["appointment"]
        if appointment is not None and appointment.free_capacity <= 0:
            raise exceptions.ParseError("no free capacity left for this appointment")

        with transaction.atomic():
            participation = serializer.save()
            email = PublicSignupEmail(participation.nanoid, [serializer.validated_data["recipient"]])
            email.send()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
