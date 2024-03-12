import os
import uuid

from collections.abc import Sequence
from typing import Self, Optional

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from users import models as user_models

from .fields import SeparatedBinaryField
from .utils.constants import *
from .utils.keys import export_privkey, get_keydir

from rest_framework import exceptions


class Research(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4())
    name = models.CharField(max_length=120, verbose_name="meno", unique=True)
    info_url = models.URLField()
    points = models.PositiveIntegerField(verbose_name="body")
    created = models.DateTimeField(auto_now_add=True)
    chosen_attribute_values = models.ManyToManyField(user_models.AttributeValue, blank=True)
    protected = models.BooleanField(default=False, null=False)
    is_published = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.name

    def change_password(self, old_raw_password, new_raw_password):
        _, encrypted_key = self.get_keypair()
        try:
            private_key = RSA.import_key(encrypted_key, old_raw_password if self.protected else "unprotected")
        except ValueError:
            raise exceptions.PermissionDenied("invalid current password")
        encrypted_key = export_privkey(private_key, new_raw_password)

        key_dir = get_keydir(self.name)
        with open(key_dir / "privatekey.der", "wb") as keyfile:
            keyfile.write(encrypted_key)
        if not self.protected:
            self.protected = True
            self.save()

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


@receiver(post_delete, sender=Research)
def keys_delete(sender, instance, created, **kwargs):
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


class EncryptedToken(models.Model):
    __AES_KEY_LENGTH = 16
    session_keys = SeparatedBinaryField(length=__AES_KEY_LENGTH)
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
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    has_participated = models.BooleanField(default=False, blank=True, null=False)
    encrypted_token = models.OneToOneField(EncryptedToken, on_delete=models.CASCADE, blank=True, null=False)
