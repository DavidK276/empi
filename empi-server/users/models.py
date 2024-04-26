import datetime
import os
import random
from collections.abc import Mapping, Sequence, Iterable
from typing import Self, Optional

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import exceptions

from .utils.keys import export_privkey, get_keydir, export_privkey_plaintext


class EmpiUserManager(UserManager):

    @staticmethod
    def new_key(user, passphrase: str):
        new_user_privkey = RSA.generate(2048)
        new_user_exported_privkey = export_privkey(new_user_privkey, passphrase)

        key_dir = get_keydir(user.username)
        key_dir.mkdir(mode=0o700, parents=True)
        with open(key_dir / "privatekey.der", "wb") as keyfile:
            keyfile.write(new_user_exported_privkey)

        new_user_exported_pubkey = new_user_privkey.publickey().export_key(format="PEM")
        with open(key_dir / "receiver.pem", "wb") as keyfile:
            keyfile.write(new_user_exported_pubkey)

        session_key = get_random_bytes(16)
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(export_privkey_plaintext(new_user_privkey))
        with open(key_dir / "privatekey.aes", "wb") as keyfile:
            keyfile.write(ciphertext)
        with open(key_dir / "privatekey.tag.aes", "wb") as tagfile:
            tagfile.write(tag)
        with open(key_dir / "privatekey.nonce.aes", "wb") as noncefile:
            noncefile.write(cipher_aes.nonce)

        for admin in EmpiUser.users.filter(~Q(pk=user.pk) & Q(is_staff=True)):
            admin_exported_pubkey, _ = admin.get_keypair()
            admin_pubkey = RSA.import_key(admin_exported_pubkey)
            cipher_rsa = PKCS1_OAEP.new(admin_pubkey)
            enc_session_key = cipher_rsa.encrypt(session_key)
            with open(key_dir / f"__admin__{admin.username}.sessionkey.rsa", "wb") as keyfile:
                keyfile.write(enc_session_key)

    @staticmethod
    def check_key_exists(username):
        if key_dir := get_keydir(username):
            return key_dir.is_dir()

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = super().create_superuser(username, email, password, **extra_fields)
        if password is not None:
            self.new_key(user, password)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        user = super().create_user(username, email, password, **extra_fields)
        if password is not None:
            self.new_key(user, password)
        return user


class EmpiUser(AbstractUser):
    users = EmpiUserManager()

    class Meta:
        default_manager_name = "users"

    def write_privkey(self, privkey: bytes):
        key_dir = get_keydir(self.username)
        with open(key_dir / "privatekey.der", "wb") as keyfile:
            keyfile.write(privkey)

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

    def get_admin_key(self, admin_username) -> Optional[bytes]:
        key_dir = get_keydir(self.username)
        admin_key_name = f"__admin__{admin_username}.sessionkey.rsa"

        if (key_dir / admin_key_name).is_file():
            with open(key_dir / admin_key_name, "rb") as keyfile:
                return keyfile.read()
        return None

    def get_backup_keys(self) -> (bytes, bytes):
        key_dir = get_keydir(self.username)

        with open(key_dir / "privatekey.aes", "rb") as keyfile:
            ciphertext = keyfile.read()
        with open(key_dir / "privatekey.tag.aes", "rb") as tagfile:
            tag = tagfile.read()
        with open(key_dir / "privatekey.nonce.aes", "rb") as noncefile:
            nonce = noncefile.read()

        return ciphertext, tag, nonce

    def change_password(self, old_raw_password, new_raw_password):
        if self.has_usable_password():
            if not self.check_password(old_raw_password):
                raise exceptions.PermissionDenied("invalid password")
        self.set_password(new_raw_password)

        _, encrypted_key = self.get_keypair()
        private_key = RSA.import_key(encrypted_key, old_raw_password)
        encrypted_key = export_privkey(private_key, new_raw_password)

        self.write_privkey(encrypted_key)

    def reset_password(self, admin: Self, admin_password: str, new_password: str):
        self.set_password(new_password)

        admin_key = self.get_admin_key(admin.username)
        if admin_key is None:
            raise exceptions.PermissionDenied("This admin has not protected this user")

        _, enc_privkey = admin.get_keypair()
        admin_privkey = RSA.import_key(enc_privkey, admin_password)
        cipher_rsa = PKCS1_OAEP.new(admin_privkey)

        decrypted_admin_sessionkey = cipher_rsa.decrypt(admin_key)
        enc_user_privkey, tag, nonce = self.get_backup_keys()

        cipher_aes = AES.new(decrypted_admin_sessionkey, AES.MODE_EAX, nonce)
        decrypted_user_privkey = cipher_aes.decrypt_and_verify(enc_user_privkey, tag)

        exported_user_privkey = export_privkey(RSA.import_key(decrypted_user_privkey), new_password)
        self.write_privkey(exported_user_privkey)

    def is_participant(self):
        return Participant.objects.filter(user=self.pk).exists()


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
