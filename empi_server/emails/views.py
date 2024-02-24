from rest_framework import viewsets

from .models import Email, Attachment
from .serializers import EmailSerializer, AttachmentSerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.get_queryset()
    serializer_class = EmailSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.get_queryset()
    serializer_class = AttachmentSerializer
