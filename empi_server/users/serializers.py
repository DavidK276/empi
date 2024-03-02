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


class AttributeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Attribute
        fields = '__all__'


class AttributeValueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AttributeValue
        fields = '__all__'


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
        fields = '__all__'
