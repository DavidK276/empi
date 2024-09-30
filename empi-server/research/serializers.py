from rest_framework import serializers

from .models import Appointment, Participation, Research


class ResearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Research
        fields = ["id", "name", "comment", "info_url", "points", "created"]


class ResearchAdminSerializer(serializers.HyperlinkedModelSerializer):
    has_open_appointments = serializers.BooleanField(read_only=True)

    class Meta:
        model = Research
        fields = [
            "nanoid",
            "name",
            "comment",
            "info_url",
            "points",
            "created",
            "is_protected",
            "is_published",
            "has_open_appointments",
            "email_recipients",
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    free_capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ["id", "appointment", "is_confirmed"]


class ParticipationUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_confirmed = serializers.BooleanField(default=False)


class AnonymousParticipationSerializer(serializers.Serializer):
    recipient = serializers.CharField(write_only=True)
    nanoid = serializers.CharField(read_only=True)
    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.get_queryset())
    appointment_detail = AppointmentSerializer(read_only=True)

    def create(self, validated_data):
        participation = Participation(appointment=validated_data["appointment"])
        participation.save()
        return participation

    def to_representation(self, instance):
        appointment = self.fields["appointment_detail"].to_representation(instance.appointment)
        return super().to_representation(instance) | {"appointment_detail": appointment}
