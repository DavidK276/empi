from rest_framework import serializers

from . import models


class ResearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Research
        fields = ["id", "name", "comment", "info_url", "points", "created"]


class ResearchAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Research
        fields = [
            "nanoid",
            "name",
            "comment",
            "info_url",
            "points",
            "created",
            "is_protected",
            "is_published",
            "email_recipients",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    free_capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Appointment
        fields = "__all__"


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participation
        fields = ["id", "appointment", "is_confirmed"]


class ParticipationUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_confirmed = serializers.BooleanField(default=False)


class AnonymousParticipationSerializer(serializers.Serializer):
    recipient = serializers.CharField(write_only=True)
    nanoid = serializers.CharField(read_only=True)
    appointment = serializers.PrimaryKeyRelatedField(queryset=models.Appointment.objects.get_queryset())
    appointment_detail = AppointmentSerializer(read_only=True)

    def create(self, validated_data):
        participation = models.Participation(appointment=validated_data["appointment"])
        participation.save()
        return participation

    def to_representation(self, instance):
        appointment = self.fields["appointment_detail"].to_representation(instance.appointment)
        return super().to_representation(instance) | {"appointment_detail": appointment}
