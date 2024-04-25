from rest_framework import serializers

from . import models


class ResearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Research
        exclude = ["chosen_attribute_values", "uuid", "email_recipients"]


class ResearchAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Research
        exclude = ["chosen_attribute_values"]
        extra_kwargs = {
            "url": {"view_name": "research-admin-detail", "lookup_field": "uuid"},
        }


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = "__all__"
        extra_kwargs = {"free_capacity": {"read_only": True}}


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participation
        fields = ["id", "appointment", "has_participated"]


class ParticipationUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    has_participated = serializers.BooleanField(default=False)


class AnonymousParticipationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    appointment = serializers.PrimaryKeyRelatedField(queryset=models.Appointment.objects.get_queryset())
    appointment_detail = AppointmentSerializer(read_only=True)

    def create(self, validated_data):
        participation = models.Participation(appointment=validated_data["appointment"])
        participation.save()
        return participation

    def to_representation(self, instance):
        appointment = self.fields["appointment_detail"].to_representation(instance.appointment)
        return super().to_representation(instance) | {"appointment_detail": appointment}
