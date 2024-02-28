import os

from Crypto.PublicKey import RSA
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .utils.constants import *
from .utils.keys import export_privkey, get_keydir


class Research(models.Model):
    name = models.CharField(max_length=120, verbose_name="meno", unique=True)
    url = models.URLField()
    points = models.PositiveIntegerField(verbose_name="body")
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def new_key(name):
        key = RSA.generate(2048)
        encrypted_key = export_privkey(key, "unprotected")

        key_dir = get_keydir(name)
        key_dir.mkdir(mode=0o700, parents=True)
        with open(key_dir / "privatekey.der", "wb") as keyfile:
            keyfile.write(encrypted_key)

        public_key = key.publickey().export_key(format="PEM")
        with open(key_dir / "receiver.pem", "wb") as keyfile:
            keyfile.write(public_key)

    def get_keypair(self) -> (bytes, bytes):
        """
        Retrieves the keypair for this user.
        :return: a tuple of the exported public key and the exported private key
        """
        key_dir = get_keydir(self.name)

        with open(key_dir / "receiver.pem", "rb") as keyfile:
            public_key = keyfile.read()
        with open(key_dir / "privatekey.der", "rb") as keyfile:
            private_key = keyfile.read()

        return public_key, private_key


@receiver(post_save, sender=Research)
def check_and_create_keys(sender, instance, **kwargs):
    key_dir = get_keydir(instance.name)
    if not key_dir.is_dir():
        Research.new_key(instance.name)


@receiver(post_delete, sender=Research)
def keys_delete(sender, instance, **kwargs):
    key_dir = get_keydir(instance.name)
    os.unlink(key_dir / "receiver.pem")
    os.unlink(key_dir / "privatekey.der")
    if len(os.listdir(key_dir)) == 0:
        key_dir.rmdir()


class Credit(models.Model):
    class RecipientType(models.TextChoices):
        LECTURER = 'LE', 'Vyučujúci'
        STUDENT = 'ST', 'Študent'
        EXPERT = 'EX', 'Expert'

    recipient_type = models.CharField(verbose_name="typ príjemcu", max_length=2, choices=RecipientType.choices)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    participant_token_encrypted = models.BinaryField()


class Appointment(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    when = models.DateTimeField(verbose_name="kedy", blank=False)
    capacity = models.IntegerField(verbose_name="kapacita")
    comment = models.TextField(blank=True)
    location = models.TextField(blank=False, null=True)
    url = models.URLField(blank=False, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(url__isnull=True) ^ Q(location__isnull=True),
                                   name="one_of_url_location_null")
        ]

    def get_type(self):
        if self.location is None:
            return AppointmentType.ONLINE
        return AppointmentType.IN_PERSON


class Participation(models.Model):
    class RecipientType(models.TextChoices):
        LECTURER = 'LE', 'vyučujúci'
        STUDENT = 'ST', 'študent'
        EXPERT = 'EX', 'expert'

    recipient_type = models.CharField(verbose_name="typ príjemcu", max_length=2, choices=RecipientType.choices)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    participant_token_encrypted = models.BinaryField()
