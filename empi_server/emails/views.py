from rest_framework import viewsets, status, mixins, permissions
from rest_framework.response import Response

from django.forms import modelform_factory

from .models import Email, Attachment
from .serializers import EmailSerializer, AttachmentSerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.get_queryset().order_by('pk')
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        form_class = modelform_factory(model=Email, fields='__all__')
        form = form_class(request.data, request.FILES)

        if form.is_valid():
            return super().create(request, *args, **kwargs)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.get('partial', False)
        fields = '__all__' if not partial else set(request.data.keys()) - {'url'}
        form_class = modelform_factory(model=Email, fields=fields)
        form = form_class(request.data, request.FILES)

        if form.is_valid():
            return super().update(request, *args, **kwargs)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class AttachmentViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Attachment.objects.get_queryset().order_by('pk')
    serializer_class = AttachmentSerializer
