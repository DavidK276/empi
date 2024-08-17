from rest_framework import serializers, validators, exceptions

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmpiUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_staff",
            "date_joined",
        ]
        extra_kwargs = {
            "password": {"style": {"input_type": "password"}, "write_only": True, "max_length": 128},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        if request := self.context.get("request"):
            if not request.user.is_staff and self.data["is_staff"]:
                raise exceptions.PermissionDenied("Creating admin users from the API is forbidden.")

        return self.Meta.model.users.create_user(**validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data.pop("password")
        return super().update(instance, validated_data)


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})
    new_password = serializers.CharField(
        max_length=100, write_only=True, default=None, style={"input_type": "password"}
    )


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, write_only=True, style={"input_type": "password"})
    passphrase = serializers.CharField(
        min_length=32, max_length=32, write_only=True, default=None, style={"input_type": "password"}
    )


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
            current_values_queryset = models.AttributeValue.objects.filter(attribute=instance)
            current_values: set[str] = {value.value for value in current_values_queryset}

            # delete values not in recieved ones
            to_delete = current_values - new_values
            current_values_queryset.filter(value__in=to_delete).delete()

            # create newly received valued
            to_create = new_values - current_values
            for value in to_create:
                attribute_value = models.AttributeValue(attribute=instance, value=value)
                attribute_value.save()
        return instance


class ParticipantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.EmpiUser.users.get_queryset().filter(is_staff=False),
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
