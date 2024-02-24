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

    def create_user(self, username, email=None, password=None, **extra_fields):
        user = super().create_user(username, email, password, **extra_fields)
        self.new_key(username, password)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = super().create_superuser(username, email, password, **extra_fields)
        self.new_key(username, password)
        return user


class EmpiUser(AbstractUser):
    objects = EmpiUserManager()

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


@receiver(post_delete, sender=EmpiUser)
def keys_delete(sender, instance, **kwargs):
    key_dir = get_keydir(instance.username)
    os.unlink(key_dir / "receiver.pem")
    os.unlink(key_dir / "privatekey.der")
    key_dir.rmdir()
    if len(os.listdir(key_dir)) == 0:
        key_dir.rmdir()


class Lecturer(models.Model):
    user = models.OneToOneField(EmpiUser, on_delete=models.CASCADE)


def generate_token():
    alphabet = ascii_uppercase + digits
    while True:
        part1 = ''.join(random.choice(alphabet) for _ in range(4))
        part2 = ''.join(random.choice(alphabet) for _ in range(4))
        result = '-'.join([part1, part2])
        user = EmpiUser.objects.get(token=result)
        if user is None:
            return result


class Participant(models.Model):
    user = models.OneToOneField(EmpiUser, on_delete=models.CASCADE)
    acad_year = models.CharField(verbose_name="akademický rok", max_length=9, blank=False, null=False,
                                 validators=[validate_acad_year])
    chosen_attribute_values = models.ManyToManyField('research.AttributeValue')
    token = models.CharField(default=generate_token, unique=True, null=False, editable=False, max_length=9)
