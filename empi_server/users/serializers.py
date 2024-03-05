from Crypto.PublicKey import RSA
from rest_framework import serializers, validators

from . import models
from .utils.keys import export_privkey, get_keydir


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.EmpiUser
        fields = [
            'url', 'username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active', 'date_joined'
        ]

    @staticmethod
    def new_key(username, passphrase: str):
        key = RSA.generate(2048)
        encrypted_key = export_privkey(key, passphrase)

        key_dir = get_keydir(username)
        key_dir.mkdir(mode=0o700, parents=True)
        with open(key_dir / "privatekey.der", "wb") as keyfile:
            keyfile.write(encrypted_key)

        public_key = key.publickey().export_key(format="PEM")
        with open(key_dir / "receiver.pem", "wb") as keyfile:
            keyfile.write(public_key)

    def create(self, validated_data):
        user = super().create(validated_data)
        self.new_key(user.username, self.validated_data['password'])
        return user


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=100, write_only=True)
    new_password = serializers.CharField(max_length=100, write_only=True, default=None)


class AttributeValueSerializer(serializers.BaseSerializer):

    def to_internal_value(self, data):
        return data

    def to_representation(self, instance: models.AttributeValue):
        return instance.value


class AttributeSerializer(serializers.HyperlinkedModelSerializer):
    # for this to work, related_name="values" must be set on the foreign key field in AttributeValue
    values = AttributeValueSerializer(many=True)

    class Meta:
        model = models.Attribute
        fields = ["url", "name", "type", "values"]

    def create(self, validated_data):
        values = validated_data.pop('values')
        attribute = models.Attribute(**validated_data)
        attribute.save()
        for value in values:
            attribute_value = models.AttributeValue(attribute=attribute, value=value)
            attribute_value.save()
        return attribute

    def update(self, instance: models.Attribute, validated_data):
        if name := validated_data.get('name', None):
            instance.name = name
            instance.save()
        if values := validated_data.get('values', None):
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


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(queryset=models.EmpiUser.objects.get_queryset(),
                                               view_name='empiuser-detail',
                                               validators=[
                                                   validators.UniqueValidator(
                                                       queryset=models.Participant.objects.get_queryset(),
                                                       message="This user is already a participant"
                                                   )
                                               ])

    class Meta:
        model = models.Participant
        exclude = ["chosen_attribute_values"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if request := self.context.get('request', None):
            if request.user.pk == instance.pk:
                attributes = dict()
                for attribute in models.Attribute.objects.all():
                    chosen_values = instance.chosen_attribute_values.filter(attribute=attribute)
                    attributes[attribute.name] = AttributeValueSerializer(chosen_values, many=True).data
                representation['attributes'] = attributes
        return representation
