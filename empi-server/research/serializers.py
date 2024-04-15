from rest_framework import serializers

from users import models as user_models
from . import models


class ResearchSerializer(serializers.HyperlinkedModelSerializer):
    protected = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Research
        exclude = ["chosen_attribute_values"]


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Appointment
        fields = "__all__"


class ParticipationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Participation
        fields = ["appointment", "has_participated"]
