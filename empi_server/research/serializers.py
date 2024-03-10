from rest_framework import serializers

from users import models as user_models
from users.serializers import AttributeValueSerializer
from . import models


class ResearchSerializer(serializers.HyperlinkedModelSerializer):
    chosen_attribute_values = AttributeValueSerializer(many=True)

    class Meta:
        model = models.Research
        fields = "__all__"

    def create(self, validated_data):
        chosen_values = validated_data.pop("chosen_attribute_values")
        attributes = {}
        for chosen_value in chosen_values:
            pk = chosen_value["attribute"].pk
            attributes.setdefault(pk, set())
            attributes[pk].add(chosen_value["value"])

        instance = super().create(validated_data)
        for pk, new_values in attributes.items():
            for value in new_values:
                try:
                    value = user_models.AttributeValue.objects.get(
                        attribute_id=pk, value=value
                    )
                    instance.chosen_attribute_values.add(value)
                except user_models.AttributeValue.DoesNotExist:
                    pass
        instance.save()
        return instance

    def update(self, instance, validated_data):
        chosen_values = validated_data.pop("chosen_attribute_values")
        attributes = {}
        for chosen_value in chosen_values:
            pk = chosen_value["attribute"].pk
            attributes.setdefault(pk, set())
            attributes[pk].add(chosen_value["value"])
        for pk, new_values in attributes.items():
            current_values_queryset = instance.chosen_attribute_values.filter(
                attribute=pk
            )
            current_values: set[str] = {
                value.value for value in current_values_queryset
            }

            to_delete = current_values - new_values
            for value_str in to_delete:
                value = instance.chosen_attribute_values.get(value=value_str)
                instance.chosen_attribute_values.remove(value)

            to_create = new_values - current_values
            for value in to_create:
                try:
                    value = user_models.AttributeValue.objects.get(
                        attribute_id=pk, value=value
                    )
                    instance.chosen_attribute_values.add(value)
                except user_models.AttributeValue.DoesNotExist:
                    pass

        return super().update(instance, validated_data)


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Appointment
        fields = "__all__"


class ParticipationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Participation
        fields = ["appointment", "has_participated"]
