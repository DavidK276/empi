from rest_framework import serializers

from . import models
from .models import Participation


class ResearchUserSerializer(serializers.ModelSerializer):
    protected = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Research
        exclude = ["chosen_attribute_values"]


class ResearchAdminSerializer(serializers.HyperlinkedModelSerializer):
    protected = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Research
        exclude = ["chosen_attribute_values"]
        extra_kwargs = {
            "url": {"view_name": "research-admin-detail", "lookup_field": "uuid"},
        }


class AppointmentSerializer(serializers.ModelSerializer):
    free_capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Appointment
        fields = "__all__"

    def to_representation(self, instance):
        instance.free_capacity = instance.capacity - Participation.objects.filter(appointment=instance).count()
        return super().to_representation(instance)


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participation
        fields = ["appointment", "has_participated"]
