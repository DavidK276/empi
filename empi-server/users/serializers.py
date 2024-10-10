from collections.abc import Iterable

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers, validators, exceptions
from rest_framework.fields import empty

from .models import AttributeValue, EmpiUser, Attribute, Participant


class UserSerializer(serializers.ModelSerializer):
    token = serializers.PrimaryKeyRelatedField(
        read_only=True,
        allow_null=True,
        source="participant.token",
    )

    class Meta:
        model = EmpiUser
        fields = ["id", "first_name", "last_name", "email", "password", "is_staff", "date_joined", "token"]
        extra_kwargs = {
            "password": {"style": {"input_type": "password"}, "write_only": True, "max_length": 128},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        return self.Meta.model.users.create_user(**validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            raw_password = validated_data.pop("password")
            instance.set_password(raw_password)
        return super().update(instance, validated_data)


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})
    new_password = serializers.CharField(
        max_length=100, write_only=True, default=None, style={"input_type": "password"}
    )


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})
    passphrase = serializers.CharField(
        min_length=64, max_length=64, write_only=True, default=None, style={"input_type": "password"}
    )


class EmailPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})
    email = serializers.EmailField(write_only=True)


class ActivateUserSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})
    passphrase = serializers.CharField(min_length=64, max_length=64, write_only=True, style={"input_type": "password"})

    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(max_length=150, write_only=True)
    last_name = serializers.CharField(max_length=150, write_only=True)


@extend_schema_field({"type": "array", "items": {"type": "string"}})
class AttributeValueField(serializers.Field):
    def run_validation(self, data=empty):
        if not isinstance(data, Iterable):
            raise exceptions.ValidationError("values must be an array of strings")
        for value in data:
            if not isinstance(value, str):
                raise exceptions.ValidationError("values must be an array of strings")
        return super().run_validation(data)

    def to_representation(self, value):
        return list(value.all().values_list("value", flat=True))

    def to_internal_value(self, data):
        return [AttributeValue(value=value) for value in data]


class AttributeSerializer(serializers.HyperlinkedModelSerializer):
    # for this to work, related_name="values" must be set on the foreign key field in AttributeValue
    values = AttributeValueField()

    class Meta:
        model = Attribute
        fields = ["url", "name", "type", "values"]

    def create(self, validated_data):
        values = validated_data.pop("values")
        attribute = Attribute(**validated_data)
        attribute.save()
        for value in values:
            attribute.values.create(value=value)
        return attribute

    def update(self, instance: Attribute, validated_data):
        if name := validated_data.get("name", None):
            instance.name = name
            instance.save(update_fields=["name"])
        if values := validated_data.get("values", None):
            AttributeValue.objects.filter(attribute=instance).delete()
            instance.values.set(values, bulk=False)
        return instance


class ParticipantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=EmpiUser.users.get_queryset().filter(is_staff=False),
        validators=[
            validators.UniqueValidator(
                queryset=Participant.objects.get_queryset(),
                message="This user is already a participant",
            )
        ],
    )
    user_detail = UserSerializer(read_only=True, source="user")

    class Meta:
        model = Participant
        exclude = ["chosen_attribute_values"]
