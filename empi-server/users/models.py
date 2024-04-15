import datetime
import os
import random
from collections.abc import Mapping, Sequence, Iterable
from typing import Self

from Crypto.PublicKey import RSA
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import exceptions

from .utils.keys import export_privkey, get_keydir


class EmpiUser(AbstractUser):

    def set_password(self, raw_password):
        super().set_password(raw_password)
        if key_dir := get_keydir(self.username):
            if not key_dir.is_dir():
                EmpiUser.new_key(self.username, raw_password)

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

    def change_password(self, old_raw_password, new_raw_password):
        if self.has_usable_password():
            if not self.check_password(old_raw_password):
                raise exceptions.PermissionDenied("invalid password")
        self.set_password(new_raw_password)

        _, encrypted_key = self.get_keypair()
        private_key = RSA.import_key(encrypted_key, old_raw_password)
        encrypted_key = export_privkey(private_key, new_raw_password)

        key_dir = get_keydir(self.username)
        with open(key_dir / "privatekey.der", "wb") as keyfile:
            keyfile.write(encrypted_key)

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
        SINGLE_CHOICE = "SC", "Výber jednej hodnoty"
        MULTIPLE_CHOICE = "MC", "Výber viacero hodnôt"
        ENTER_TEXT = "ET", "Vpis textu"

    name = models.CharField(max_length=150, blank=False, unique=True)
    type = models.CharField(max_length=2, choices=AttributeType.choices, default=AttributeType.SINGLE_CHOICE)

    def __str__(self):
        return self.name.capitalize()


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        verbose_name="atribút",
        related_name="values",
        on_delete=models.CASCADE,
    )
    value = models.CharField(verbose_name="hodnota", max_length=150, blank=False)

    class Meta:
        constraints = [models.UniqueConstraint("attribute", "value", name="unique_value_per_attribute")]

    def __str__(self):
        return "%s > %s" % (str(self.attribute), self.value.capitalize())

    @classmethod
    def group_by_attribute(cls, queryset: Iterable[Self], all=False) -> Mapping[str : Sequence[str]]:
        result = {}
        if all:
            for attr in Attribute.objects.all():
                result[attr.name] = []
        for value in queryset:
            result.setdefault(value.attribute.name, [])
            result[value.attribute.name].append(value.value)
        return result

    @classmethod
    def from_groups(cls, groups: Mapping[str : Sequence[str]]) -> Iterable[Self]:
        result = []
        for name, values in groups.items():
            result.extend(cls.objects.filter(attribute__name=name).filter(value__in=values))
        return result


def generate_token():
    alphabet = "2346789BCDFGHJKMPQRTVWXY"
    while True:
        part1 = "".join(random.choice(alphabet) for _ in range(4))
        part2 = "".join(random.choice(alphabet) for _ in range(4))
        result = f"{part1}-{part2}"
        try:
            Participant.objects.get(token=result)
        except Participant.DoesNotExist:
            return result


def generate_acad_year():
    now = datetime.datetime.now()
    if now.month >= 8:
        year = now.year
    else:
        year = now.year - 1
    return f"{year}/{(year + 1) % 100}"


class Participant(models.Model):
    user = models.OneToOneField(EmpiUser, on_delete=models.CASCADE, primary_key=True)
    acad_year = models.CharField(verbose_name="akademický rok", default=generate_acad_year, max_length=7)
    chosen_attribute_values = models.ManyToManyField(AttributeValue, related_name="attributes", blank=True)
    token = models.CharField(default=generate_token, unique=True, null=False, editable=False, max_length=9)
