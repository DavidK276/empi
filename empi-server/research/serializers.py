from rest_framework import serializers

from .models import Participation
from . import models


class ResearchSerializer(serializers.HyperlinkedModelSerializer):
    protected = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Research
        exclude = ["chosen_attribute_values"]


class AppointmentSerializer(serializers.ModelSerializer):
    free_capacity = serializers.IntegerField()

    class Meta:
        model = models.Appointment
        fields = "__all__"

    def to_representation(self, instance):
        instance.free_capacity = instance.capacity - Participation.objects.filter(appointment=instance).count()
        return super().to_representation(instance)


class ParticipationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Participation
        fields = ["appointment", "has_participated"]
