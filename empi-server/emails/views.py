from http import HTTPMethod

from Crypto.PublicKey import RSA
from knox.auth import TokenAuthentication
from rest_framework import viewsets, status, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.forms import modelform_factory

from research.auth import ResearchAuthentication
from research.models import Research, Participation
from users.models import EmpiUser
from .models import Email, Attachment
from .serializers import EmailSerializer, AttachmentSerializer, ResearchEmailSerializer
from .types import ResearchInfoEmail


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.get_queryset().order_by("pk")
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [ResearchAuthentication, TokenAuthentication, SessionAuthentication]

    def create(self, request, *args, **kwargs):
        form_class = modelform_factory(model=Email, fields="__all__")
        form = form_class(request.data, request.FILES)

        if form.is_valid():
            return super().create(request, *args, **kwargs)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.get("partial", False)
        fields = "__all__" if not partial else set(request.data.keys()) - {"url"}
        form_class = modelform_factory(model=Email, fields=fields)
        form = form_class(request.data, request.FILES)

        if form.is_valid():
            return super().update(request, *args, **kwargs)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=[HTTPMethod.POST])
    def send(self, request, pk=None):
        email = self.get_object()
        email.send()
        return Response()

    @action(detail=False, methods=[HTTPMethod.POST], serializer_class=ResearchEmailSerializer)
    def send_research_info(self, request):
        serializer: ResearchEmailSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        research: Research = get_object_or_404(Research, nanoid=serializer.validated_data.pop("research_nanoid"))

        _, encrypted_privkey = research.get_keypair()
        private_key = RSA.import_key(encrypted_privkey, passphrase=serializer.validated_data.pop("research_password"))

        interesting_participations = Participation.objects.all().filter(
            appointment=serializer.validated_data.pop("appointment")
        )

        tokens = []
        for p in interesting_participations:
            if token := p.decrypt(private_key):
                tokens.append(token)

        recipients = list(EmpiUser.users.all().filter(participant__token__in=tokens).values_list("email", flat=True))

        recipients.extend(serializer.validated_data.pop("extra_recipients").replace(" ", "").split(","))

        email = ResearchInfoEmail(research=research, recipients=recipients, **serializer.validated_data)
        email.send()

        return Response()


class AttachmentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Attachment.objects.get_queryset().order_by("pk")
    serializer_class = AttachmentSerializer
