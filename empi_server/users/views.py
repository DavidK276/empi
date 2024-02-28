from http import HTTPMethod

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import EmpiUser, Participant, Attribute, AttributeValue
from .serializers import UserSerializer, PasswordSerializer, ParticipantSerializer, AttributeSerializer, \
    AttributeValueSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = EmpiUser.users.get_queryset().order_by('date_joined')
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer: UserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['is_staff']:
            EmpiUser.users.create_superuser(**serializer.validated_data)
        else:
            EmpiUser.users.create_user(**serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, name="Change password", methods=[HTTPMethod.POST], serializer_class=PasswordSerializer)
    def change_password(self, request, pk=None):
        user: EmpiUser = self.get_object()
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        if not user.check_password(current_password):
            return Response({'status': 'invalid current password'}, status=status.HTTP_401_UNAUTHORIZED)
        user.change_password(current_password, new_password)
        user.save()
        return Response({'status': 'password changed'})

    @action(detail=True, name="Get attributes", methods=[HTTPMethod.GET], serializer_class=PasswordSerializer)
    def get_attributes(self, request, pk=None):
        ...


class ParticipantViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Participant.objects.get_queryset().order_by('pk')
    serializer_class = ParticipantSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.get_queryset().order_by('pk')
    serializer_class = AttributeSerializer


class AttributeValueViewSet(viewsets.ModelViewSet):
    queryset = AttributeValue.objects.get_queryset().order_by('pk')
    serializer_class = AttributeValueSerializer
