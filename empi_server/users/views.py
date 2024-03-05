from collections.abc import Iterable
from http import HTTPMethod

from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, status, mixins, exceptions, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import EmpiUser, Participant, Attribute, AttributeValue
from .serializers import UserSerializer, PasswordSerializer, ParticipantSerializer, AttributeSerializer, \
    AttributeValueSerializer

from research.models import Research


class UserViewSet(viewsets.ModelViewSet):
    queryset = EmpiUser.objects.get_queryset().order_by('date_joined')
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user: EmpiUser = serializer.instance
        user.set_password(serializer.validated_data['password'])
        user.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, name="Change password", methods=[HTTPMethod.POST], serializer_class=PasswordSerializer)
    def change_password(self, request, pk=None):
        user: EmpiUser = self.get_object()
        if isinstance(request.user, AnonymousUser) or request.user == self.get_object():
            raise exceptions.AuthenticationFailed('only changing own password is allowed')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        if not user.check_password(current_password):
            raise exceptions.NotFound('invalid current password')
        user.change_password(current_password, new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)


class ParticipantViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Participant.objects.get_queryset().order_by('pk')
    serializer_class = ParticipantSerializer


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.get_queryset().order_by('pk')
    serializer_class = AttributeSerializer

    @staticmethod
    def chosen_values_to_dict(chosen_values: Iterable[AttributeValue]):
        attributes_obj: dict[str: dict] = {}
        for chosen_value in chosen_values:
            attribute = Attribute.objects.get(pk=chosen_value.attribute)
            values = AttributeValue.objects.filter(attribute=attribute)
            attribute_obj = {"type": attribute.type}
            values_obj = {}
            for value in values:
                values_obj[value.value] = (value == chosen_value)
            attribute_obj["values"] = values_obj
            attributes_obj[attribute.name] = attribute_obj
        return attributes_obj

    @action(detail=False, name="Get attributes for participant", methods=[HTTPMethod.GET])
    def for_participant(self, request):
        if isinstance(request.user, AnonymousUser):
            raise exceptions.AuthenticationFailed('only viewing own attributes is allowed')
        try:
            participant: Participant = Participant.objects.get(user=request.user.pk)
        except Participant.DoesNotExist:
            raise exceptions.NotFound('user is not a participant')
        chosen_values = participant.chosen_attribute_values.all()
        attributes = Attribute.objects.all()
        serializer = AttributeSerializer(attributes, many=True, context={'request': request})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

    @action(detail=False, name="Get attributes for user", methods=[HTTPMethod.GET])
    def participant(self, request):
        if isinstance(request.user, AnonymousUser) or request.user == self.get_object():
            raise exceptions.AuthenticationFailed('only viewing own attributes is allowed')
        pk = request.GET.get('participant', None)
        try:
            participant: Participant = Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            raise exceptions.NotFound('participant does not exist')
        return Response(self.chosen_values_to_dict(participant.chosen_attribute_values.all()))

    @action(detail=False, name="Get attributes for research", methods=[HTTPMethod.GET])
    def research(self, request):
        pk = request.GET.get('research', None)
        try:
            research: Research = Research.objects.get(pk=pk)
        except Research.DoesNotExist:
            raise exceptions.NotFound('research does not exist')
        return Response(self.chosen_values_to_dict(research.chosen_attribute_values.all()))


class AttributeValueViewSet(viewsets.ModelViewSet):
    queryset = AttributeValue.objects.get_queryset().order_by('pk')
    serializer_class = AttributeValueSerializer
