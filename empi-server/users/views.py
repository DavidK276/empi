from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from nanoid import generate
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.routers import reverse
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from emails.types import PasswordResetEmail, AdminCreatedEmail
from research.models import Research, Participation
from .models import EmpiUser, Participant, Attribute, AttributeValue, ResetKey, EncryptedSessionKey
from .permissions import *
from .serializers import (
    UserSerializer,
    PasswordChangeSerializer,
    ParticipantSerializer,
    AttributeSerializer,
    PasswordResetSerializer,
    PasswordSerializer,
    ActivateUserSerializer,
    EmailPasswordSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = EmpiUser.users.get_queryset().filter(is_active=True).order_by("date_joined")
    serializer_class = UserSerializer
    permission_classes = [(IsAuthenticatedOrReadOnly & IsSelf) | IsAdminUser]

    @action(
        detail=True,
        name="Change password",
        methods=[HTTPMethod.POST],
        serializer_class=PasswordChangeSerializer,
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
            raise exceptions.AuthenticationFailed(_("invalid current password"))
        user.change_password(current_password, new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        name="Change password by admin",
        methods=[HTTPMethod.POST],
        serializer_class=PasswordChangeSerializer,
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
        detail=False,
        methods=[HTTPMethod.POST],
        serializer_class=EmailPasswordSerializer,
        permission_classes=[IsAdminUser],
    )
    def start_password_reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: EmpiUser = get_object_or_404(EmpiUser, email=serializer.validated_data["email"])
        admin_password = serializer.validated_data["password"]
        passphrase = user.make_reset_key(request.user, admin_password)

        email = PasswordResetEmail(user.pk, passphrase, [user.email])
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

        return Response(status=HTTP_204_NO_CONTENT)

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
        if user.check_password(request.data["password"]):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, name="Get own details", methods=[HTTPMethod.GET], permission_classes=[IsAuthenticated])
    def get_self(self, request):
        return HttpResponseRedirect(reverse("empiuser-detail", [request.user.id], request=request))

    @action(
        detail=False,
        name="Create admin",
        methods=[HTTPMethod.POST],
        permission_classes=[IsAdminUser],
        serializer_class=EmailPasswordSerializer,
    )
    def create_admin(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            _ = EmpiUser.users.get(email=serializer.validated_data["email"])
            raise exceptions.ValidationError(detail={"detail": "Tento email sa už používa"})
        except EmpiUser.DoesNotExist:
            pass

        current_admin: EmpiUser = request.user
        passphrase = serializer.validated_data["password"]
        if not current_admin.check_password(passphrase):
            raise exceptions.AuthenticationFailed()

        new_admin_email = serializer.validated_data["email"]
        activation_code = generate(alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", size=64)

        with transaction.atomic():
            new_admin = EmpiUser.users.create_superuser(
                email=new_admin_email, password=activation_code, is_active=False
            )
            new_admin_pubkey = RSA.import_key(new_admin.pubkey)

            current_admin_privkey = RSA.import_key(current_admin.privkey, passphrase)
            for participation in Participation.objects.all():
                token = participation.decrypt(current_admin_privkey)
                participation.add_encrypted_token(token, new_admin_pubkey)
                participation.save()

            for user in EmpiUser.users.all().exclude(pk=new_admin.pk):
                session_key_encrypted_by_current_admin = EncryptedSessionKey.objects.get(
                    admin=current_admin, backup_key=user.backup_privkey
                )
                cipher_rsa = PKCS1_OAEP.new(current_admin_privkey)
                session_key = cipher_rsa.decrypt(session_key_encrypted_by_current_admin.data)

                cipher_rsa = PKCS1_OAEP.new(new_admin_pubkey)
                enc_session_key = EncryptedSessionKey(
                    admin=new_admin, backup_key=user.backup_privkey, data=cipher_rsa.encrypt(session_key)
                )
                enc_session_key.save()

            email = AdminCreatedEmail(new_admin.pk, passphrase=activation_code, recipients=[new_admin_email])
            email.send()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        name="Activate account",
        methods=[HTTPMethod.POST],
        permission_classes=[AllowAny],
        serializer_class=ActivateUserSerializer,
        queryset=EmpiUser.users.get_queryset().filter(is_active=False),
    )
    def activate_account(self, request, pk: int):
        serializer: ActivateUserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user: EmpiUser = self.get_object()
            user.change_password(serializer.validated_data["passphrase"], serializer.validated_data["new_password"])

            user.is_active = True
            user.email = serializer.validated_data["email"]
            user.first_name = serializer.validated_data["first_name"]
            user.last_name = serializer.validated_data["last_name"]
            user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


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
    lookup_field = "token"

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
