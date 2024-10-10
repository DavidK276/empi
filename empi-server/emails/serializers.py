from rest_framework import serializers

from research.models import Appointment
from . import models


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = "__all__"


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Attachment
        fields = "__all__"


class ResearchEmailSerializer(serializers.Serializer):
    extra_recipients = serializers.CharField()
    subject = serializers.CharField()
    body = serializers.CharField()

    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.get_queryset(), required=False)
    research_nanoid = serializers.CharField()
    research_password = serializers.CharField(style={"input_type": "password"})
