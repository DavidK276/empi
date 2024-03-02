from rest_framework import serializers

from . import models


class ResearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Research
        fields = '__all__'


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Appointment
        fields = '__all__'


class ParticipationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Participation
        fields = ['appointment', 'has_participated']

