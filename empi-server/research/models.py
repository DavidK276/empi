import os
from collections.abc import Sequence
from typing import Self, Optional

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, Manager
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import exceptions

from empi_server.fields import SeparatedValuesField
from users import models as user_models
from .fields import SeparatedBinaryField
from .utils.constants import *
from .utils.keys import export_privkey, get_keydir
from .utils.misc import generate_nanoid


class ResearchManager(Manager):

    def create(self, **kwargs):
        research: Research = super().create(**kwargs)
        research.new_key()
        return research


class Research(models.Model):
    objects = ResearchManager()

    nanoid = models.CharField(max_length=20, unique=True, editable=False, default=generate_nanoid)
    name = models.CharField(max_length=120, verbose_name="meno", unique=True)
    info_url = models.URLField()
    points = models.PositiveIntegerField(verbose_name="body", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    chosen_attribute_values = models.ManyToManyField(user_models.AttributeValue, blank=True)
    is_protected = models.BooleanField(default=False, editable=False)
    is_published = models.BooleanField(default=False, null=False)
    email_recipients = SeparatedValuesField(verbose_name="príjemcovia", field=models.EmailField)

    def __str__(self):
        return self.name

    def change_password(self, old_raw_password, new_raw_password):
        _, encrypted_key = self.get_keypair()
        try:
            private_key = RSA.import_key(encrypted_key, old_raw_password if self.is_protected else "unprotected")
        except ValueError:
            raise exceptions.PermissionDenied("invalid current password")
        encrypted_key = export_privkey(private_key, new_raw_password)

        key_dir = get_keydir(self.name)
        with open(key_dir / "privatekey.der", "wb") as keyfile:
            keyfile.write(encrypted_key)
        if not self.is_protected:
            self.is_protected = True
            self.save()

    def new_key(self):
        key = RSA.generate(2048)
        encrypted_key = export_privkey(key, "unprotected")

        key_dir = get_keydir(self.name)
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


@receiver(post_delete, sender=Research)
def keys_delete(sender, instance, **kwargs):
    key_dir = get_keydir(instance.name)
    os.unlink(key_dir / "receiver.pem")
    os.unlink(key_dir / "privatekey.der")
    if len(os.listdir(key_dir)) == 0:
        key_dir.rmdir()


class Appointment(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    when = models.DateTimeField(verbose_name="kedy", blank=False)
    capacity = models.IntegerField(verbose_name="kapacita")
    comment = models.TextField(blank=True)
    location = models.TextField(blank=False, null=True)
    info_url = models.URLField(blank=False, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(info_url__isnull=True) ^ Q(location__isnull=True),
                name="one_of_url_location_null",
            )
        ]

    def __str__(self):
        return " / ".join((self.research.name, self.when.isoformat(timespec="minutes")))

    def get_type(self):
        if self.location is None:
            return AppointmentType.ONLINE
        return AppointmentType.IN_PERSON

    def get_pubkeys(self, user) -> Sequence[RsaKey]:
        pubkeys = []
        public_key_bytes, _ = self.research.get_keypair()
        pubkeys.append(RSA.import_key(public_key_bytes))

        public_key_bytes, _ = user.get_keypair()
        pubkeys.append(RSA.import_key(public_key_bytes))

        admins = get_user_model().objects.filter(is_staff=True)
        for admin in admins:
            public_key_bytes, _ = admin.get_keypair()
            pubkeys.append(RSA.import_key(public_key_bytes))
        return pubkeys

    @property
    def free_capacity(self) -> int:
        return self.capacity - Participation.objects.filter(appointment=self).count()


class EncryptedToken(models.Model):
    __AES_KEY_LENGTH = 16
    session_keys = SeparatedBinaryField()
    nonce = models.BinaryField()
    tag = models.BinaryField()
    ciphertext = models.BinaryField()

    @classmethod
    def new(cls, token: str, pubkeys: Sequence[RsaKey]) -> Self:
        session_key = get_random_bytes(cls.__AES_KEY_LENGTH)
        enc_session_keys = []
        for pubkey in pubkeys:
            cipher_rsa = PKCS1_OAEP.new(pubkey)
            enc_session_keys.append(cipher_rsa.encrypt(session_key))

        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(token.encode("utf-8"))

        del session_key  # the session key is sensitive, so delete it immediately
        return cls(
            session_keys=enc_session_keys,
            nonce=cipher_aes.nonce,
            tag=tag,
            ciphertext=ciphertext,
        )

    def decrypt(self, private_key: RsaKey) -> Optional[str]:
        cipher_rsa = PKCS1_OAEP.new(private_key)
        for enc_key in self.session_keys:
            try:
                session_key = cipher_rsa.decrypt(enc_key)
            except ValueError:
                continue
            if len(session_key) != self.__AES_KEY_LENGTH:  # anything else means decryption failed
                continue
            cipher_aes = AES.new(session_key, AES.MODE_EAX, self.nonce)
            try:
                token_data = cipher_aes.decrypt_and_verify(self.ciphertext, self.tag)
            except ValueError:
                continue
            token = token_data.decode("utf-8")

            del session_key  # the session key is sensitive, so delete it immediately
            return token
        return None


class Participation(models.Model):
    nanoid = models.CharField(max_length=20, unique=True, editable=False, default=generate_nanoid)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    has_participated = models.BooleanField(default=False, blank=True, null=False)
    encrypted_token = models.OneToOneField(EncryptedToken, on_delete=models.CASCADE, blank=True, null=True)
