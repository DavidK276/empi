from rest_framework import serializers, validators

from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.EmpiUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active', 'date_joined',
            'last_login', 'url'
        ]


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)


class LecturerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(queryset=models.EmpiUser.users.all(), view_name='empiuser-detail',
                                               validators=[
                                                   validators.UniqueValidator(
                                                       queryset=models.Lecturer.objects.all(),
                                                       message="This user is already a lecturer"
                                                   )
                                               ])

    class Meta:
        model = models.Lecturer
        fields = '__all__'


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(queryset=models.EmpiUser.users.all(), view_name='empiuser-detail',
                                               validators=[
                                                   validators.UniqueValidator(
                                                       queryset=models.Participant.objects.all(),
                                                       message="This user is already a participant"
                                                   )
                                               ])

    class Meta:
        model = models.Participant
        fields = '__all__'
