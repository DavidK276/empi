import os
import random
from string import ascii_uppercase, digits

from Crypto.PublicKey import RSA
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .utils import constants
from .utils.keys import export_privkey, get_keydir
from .utils.validators import validate_acad_year


class EmpiUserManager(UserManager):
    pass


class EmpiUser(AbstractUser):

    def get_keypair(self) -> (bytes, bytes):
        """
        Retrieves the keypair for this user.
        :return: a tuple of the exported public key and the exported private key
        """
        key_dir = get_keydir(self.username)

        with open(key_dir / "receiver.pem", "rb") as keyfile:
            public_key = keyfile.read()
        with open(key_dir / "privatekey.der", "rb") as keyfile:
            private_key = keyfile.read()

        return public_key, private_key

    def change_password(self, old_raw_password, new_raw_password) -> int:
        if self.has_usable_password():
            if not self.check_password(old_raw_password):
                return constants.INVALID_PASSPHRASE
        self.set_password(new_raw_password)

        _, encrypted_key = self.get_keypair()
        private_key = RSA.import_key(encrypted_key, old_raw_password)
        encrypted_key = export_privkey(private_key, new_raw_password)

        key_dir = get_keydir(self.username)
        with open(key_dir / "privatekey.der", "wb") as keyfile:
            keyfile.write(encrypted_key)

        return 0

    def is_participant(self):
        try:
            _ = Participant.objects.get(user=self.pk)
            return True
        except Participant.DoesNotExist:
            return False


@receiver(post_delete, sender=EmpiUser)
def keys_delete(sender, instance, **kwargs):
    key_dir = get_keydir(instance.username)
    if key_dir.is_dir():
        if (key_dir / "receiver.pem").is_file():
            os.unlink(key_dir / "receiver.pem")
        if (key_dir / "privatekey.der").is_file():
            os.unlink(key_dir / "privatekey.der")
        if len(os.listdir(key_dir)) == 0:
            key_dir.rmdir()


class Attribute(models.Model):
    class AttributeType(models.TextChoices):
        SINGLE_CHOICE = 'SC', 'Výber jednej hodnoty'
        MULTIPLE_CHOICE = 'MC', 'Výber viacero hodnôt'
        ENTER_TEXT = 'ET', 'Vpis textu'

    name = models.CharField(max_length=150, blank=False)
    type = models.CharField(max_length=2, choices=AttributeType.choices, default=AttributeType.SINGLE_CHOICE)

    def __str__(self):
        return self.name.capitalize()


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, verbose_name="atribút", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="hodnota", max_length=150, blank=False)

    def __str__(self):
        return "%s > %s" % (str(self.attribute), self.name.capitalize())


def generate_token():
    alphabet = ascii_uppercase + digits
    while True:
        part1 = ''.join(random.choice(alphabet) for _ in range(4))
        part2 = ''.join(random.choice(alphabet) for _ in range(4))
        result = '-'.join([part1, part2])
        try:
            Participant.objects.get(token=result)
        except Participant.DoesNotExist:
            return result


class Participant(models.Model):
    user = models.OneToOneField(EmpiUser, on_delete=models.CASCADE, primary_key=True)
    acad_year = models.CharField(verbose_name="akademický rok", max_length=9, blank=False, null=False,
                                 validators=[validate_acad_year])
    chosen_attribute_values = models.ManyToManyField(AttributeValue, blank=True)
    token = models.CharField(default=generate_token, unique=True, null=False, editable=False, max_length=9)
