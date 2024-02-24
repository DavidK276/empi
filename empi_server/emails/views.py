from rest_framework import viewsets, status
from django.core.mail import send_mail
from rest_framework.response import Response

from .forms import EmailForm
from .models import Email, Attachment
from .serializers import EmailSerializer, AttachmentSerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.get_queryset().order_by('pk')
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            return super().update(request, *args, **kwargs)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            return super().update(request, *args, **kwargs)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        emails = super().retrieve(request, *args, **kwargs)
        return emails


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.get_queryset().order_by('pk')
    serializer_class = AttachmentSerializer
