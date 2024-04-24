from rest_framework import serializers

from . import models


class ResearchUserSerializer(serializers.ModelSerializer):
    protected = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Research
        exclude = ["chosen_attribute_values", "uuid"]


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


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Participation
        fields = ["id", "appointment", "has_participated"]


class ParticipationUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    has_participated = serializers.BooleanField(default=False)


class AnonymousParticipationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    appointment = serializers.PrimaryKeyRelatedField(
        queryset=models.Appointment.objects.get_queryset()
    )
    appointment_detail = AppointmentSerializer(read_only=True)

    def create(self, validated_data):
        participation = models.Participation(appointment=validated_data["appointment"])
        participation.save()
        return participation

    def to_representation(self, instance):
        appointment = self.fields['appointment_detail'].to_representation(instance.appointment)
        return super().to_representation(instance) | {'appointment_detail': appointment}
