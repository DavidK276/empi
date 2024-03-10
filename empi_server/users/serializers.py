from Crypto.PublicKey import RSA
from rest_framework import serializers, validators

from . import models
from .models import Attribute
from .utils.keys import export_privkey, get_keydir


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.EmpiUser
        fields = [
            "url",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_staff",
            "is_active",
            "date_joined",
        ]

    def create(self, validated_data):
        user = super().create(validated_data)
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=100, write_only=True)
    new_password = serializers.CharField(max_length=100, write_only=True, default=None)


class AttributeValueSimpleSerializer(serializers.BaseSerializer):

    def to_internal_value(self, data):
        return data

    def to_representation(self, instance: models.AttributeValue):
        return instance.value


class AttributeSerializer(serializers.HyperlinkedModelSerializer):
    # for this to work, related_name="values" must be set on the foreign key field in AttributeValue
    values = AttributeValueSimpleSerializer(many=True)

    class Meta:
        model = models.Attribute
        fields = ["url", "name", "type", "values"]

    def create(self, validated_data):
        values = validated_data.pop("values")
        attribute = models.Attribute(**validated_data)
        attribute.save()
        for value in values:
            attribute_value = models.AttributeValue(attribute=attribute, value=value)
            attribute_value.save()
        return attribute

    def update(self, instance: models.Attribute, validated_data):
        if name := validated_data.get("name", None):
            instance.name = name
            instance.save()
        if values := validated_data.get("values", None):
            new_values = set(values)
            current_values_queryset = models.AttributeValue.objects.filter(
                attribute=instance
            )
            current_values: set[str] = {
                value.value for value in current_values_queryset
            }

            # delete values not in recieved ones
            to_delete = current_values - new_values
            current_values_queryset.filter(value__in=to_delete).delete()

            # create newly received valued
            to_create = new_values - current_values
            for value in to_create:
                attribute_value = models.AttributeValue(attribute=instance, value=value)
                attribute_value.save()
        return instance


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=models.EmpiUser.objects.get_queryset(),
        view_name="empiuser-detail",
        validators=[
            validators.UniqueValidator(
                queryset=models.Participant.objects.get_queryset(),
                message="This user is already a participant",
            )
        ],
    )

    class Meta:
        model = models.Participant
        exclude = ["chosen_attribute_values"]

    @property
    def data(self):
        data = super().data
        return data

    @property
    def validated_data(self):
        data = super().validated_data
        return data

    def create(self, validated_data):
        instance = super().create(validated_data)
        if chosen_values := validated_data.pop("chosen_attribute_values", None):
            attributes = {}
            for chosen_value in chosen_values:
                pk = chosen_value["attribute"].pk
                attributes.setdefault(pk, set())
                attributes[pk].add(chosen_value["value"])

            for pk, new_values in attributes.items():
                for value in new_values:
                    try:
                        value = models.AttributeValue.objects.get(
                            attribute_id=pk, value=value
                        )
                        instance.chosen_attribute_values.add(value)
                    except models.AttributeValue.DoesNotExist:
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
                    value = models.AttributeValue.objects.get(
                        attribute_id=pk, value=value
                    )
                    instance.chosen_attribute_values.add(value)
                except models.AttributeValue.DoesNotExist:
                    pass
        return super().update(instance, validated_data)
