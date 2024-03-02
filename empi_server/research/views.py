from collections.abc import Iterable
from http import HTTPMethod

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, mixins, status, exceptions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from users.models import Participant
from users.serializers import PasswordSerializer

from .models import Appointment, Research, Participation
from .serializers import AppointmentSerializer, ResearchSerializer, ParticipationSerializer
from .utils.keys import parse_encrypted_data, encrypt_token


class ResearchViewSet(viewsets.ModelViewSet):
    queryset = Research.objects.get_queryset().order_by('-created')
    serializer_class = ResearchSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.get_queryset().order_by('pk')
    serializer_class = AppointmentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data + {'type': instance.get_type()})


class ParticipationViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = Participation.objects.get_queryset().order_by('pk')
    serializer_class = ParticipationSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            raise exceptions.NotAuthenticated()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = Participant.objects.get(pk=request.user.pk).token
        except Participant.DoesNotExist:
            raise exceptions.NotFound('user is not a participant')

        try:
            appointment: Appointment = serializer.validated_data['appointment']
            public_key_bytes, _ = appointment.research.get_keypair()
            pubkey = RSA.import_key(public_key_bytes)
            token_encrypted = encrypt_token(token, pubkey)
            participation = Participation(recipient_type='EX', appointment=appointment,
                                          token_encrypted=token_encrypted)
            participation.save()

            public_key_bytes, _ = request.user.get_keypair()
            pubkey = RSA.import_key(public_key_bytes)
            token_encrypted = encrypt_token(token, pubkey)
            participation = Participation(recipient_type='ST', appointment=appointment,
                                          token_encrypted=token_encrypted)
            participation.save()

            admins = get_user_model().objects.filter(is_staff=True)
            for admin in admins:
                public_key_bytes, _ = admin.get_keypair()
                pubkey = RSA.import_key(public_key_bytes)
                token_encrypted = encrypt_token(token, pubkey)
                participation = Participation(recipient_type='LE', appointment=appointment,
                                              token_encrypted=token_encrypted)
                participation.save()
            return Response(status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            raise exceptions.ParseError('the specified appointment was not found')

    @staticmethod
    def get_participations_for_key(private_key: RsaKey, credits: Iterable[Participation], request):
        result = []
        for credit in credits:
            enc_session_key, nonce, tag, ciphertext = parse_encrypted_data(credit.token_encrypted,
                                                                           private_key.size_in_bytes())
            cipher_rsa = PKCS1_OAEP.new(private_key)
            try:
                session_key = cipher_rsa.decrypt(enc_session_key)
            except ValueError:
                continue

            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            token_data = cipher_aes.decrypt_and_verify(ciphertext, tag)
            token = token_data.decode('utf-8')
            data = ParticipationSerializer(credit, context={'request': request}).data | {'token': token}

            result.append(data)
        return result

    @staticmethod
    def get_user_participations(request: Request) -> Response:
        # serializer = PasswordSerializer(data=request.data)
        serializer = PasswordSerializer(data={"current_password": "asdf"})  # for testing
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data['current_password']
        if not request.user.check_password(password):
            return Response({'status': 'invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

        role = 'LE' if request.user.is_staff else 'ST'
        credits = Participation.objects.filter(recipient_type=role)

        _, encrypted_key = request.user.get_keypair()
        private_key = RSA.import_key(encrypted_key, password)

        return Response(ParticipationViewSet.get_participations_for_key(private_key, credits, request))

    @staticmethod
    def get_research_participations(request: Request) -> Response:
        try:
            research: Research = Research.objects.get(pk=request.GET['research'])
            _, encrypted_key = research.get_keypair()
            private_key = RSA.import_key(encrypted_key, "unprotected")

            credits = Participation.objects.filter(recipient_type='EX')
            return Response(ParticipationViewSet.get_participations_for_key(private_key, credits, request))
        except Research.DoesNotExist:
            raise exceptions.NotFound('the specified research does not exist')

    @action(detail=False, name="Get decrypted", methods=[HTTPMethod.GET])
    def get_decrypted_participations(self, request: Request):
        research_id = request.GET.get('research', default=None)
        if research_id:
            return self.get_research_participations(request)
        if not isinstance(request.user, AnonymousUser):
            return self.get_user_participations(request)
        raise exceptions.ParseError('missing research query parameter')
