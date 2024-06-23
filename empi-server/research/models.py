import datetime
from collections.abc import Sequence, Mapping
from typing import Self, Optional

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, Manager
from django.forms import model_to_dict
from rest_framework import exceptions

from empi_server.fields import SeparatedValuesField
from users.models import EmpiUser, AttributeValue
from .fields import SeparatedBinaryField
from .utils.constants import *
from utils.keys import export_privkey, export_privkey_plaintext
from .utils.misc import generate_nanoid


class ResearchManager(Manager):

    @staticmethod
    def init_keys(password: str):
        new_user_privkey = RSA.generate(2048)
        privkey = export_privkey(new_user_privkey, password)
        pubkey = new_user_privkey.publickey().export_key(format="PEM")

        session_key = get_random_bytes(16)
        nonce = get_random_bytes(16)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce=nonce, mac_len=16)
        ciphertext, tag = cipher_aes.encrypt_and_digest(export_privkey_plaintext(new_user_privkey))

        backup_privkey = BackupKey(nonce=nonce, tag=tag, backup_key=ciphertext)
        backup_privkey.save()

        for admin in EmpiUser.users.filter(is_staff=True):
            admin_pubkey = RSA.import_key(admin.pubkey)
            cipher_rsa = PKCS1_OAEP.new(admin_pubkey)
            enc_session_key = EncryptedSessionKey(
                admin=admin,
                backup_key=backup_privkey,
                data=cipher_rsa.encrypt(session_key)
            )
            enc_session_key.save()
        return {
            "privkey": privkey,
            "pubkey": pubkey,
            "backup_privkey": backup_privkey
        }

    def get_queryset(self):
        return super().get_queryset().defer("pubkey", "privkey", "backup_privkey")

    def create(self, **kwargs):
        return super().create(**(kwargs | self.init_keys("unprotected")))


class EncryptedSessionKey(models.Model):
    admin = models.ForeignKey('Research', on_delete=models.CASCADE)
    backup_key = models.ForeignKey('BackupKey', on_delete=models.CASCADE)

    data = models.BinaryField(max_length=1024)


class BackupKey(models.Model):
    nonce = models.BinaryField(max_length=16)
    tag = models.BinaryField(max_length=16)
    backup_key = models.BinaryField(max_length=4096)


class ResetKey(models.Model):
    user = models.OneToOneField('Research', on_delete=models.CASCADE)
    valid_until = models.DateTimeField()
    backup_key = models.BinaryField(max_length=4096)

    @classmethod
    def new(cls, user, backup_key: bytes):
        try:
            ResetKey.objects.get(user=user.pk).delete()
        except ResetKey.DoesNotExist:
            pass
        valid_until = datetime.datetime.now() + datetime.timedelta(hours=12)
        return cls(valid_until=valid_until, backup_key=backup_key)


class Research(models.Model):
    objects = ResearchManager()

    nanoid = models.CharField(max_length=20, unique=True, editable=False, default=generate_nanoid)
    name = models.CharField(max_length=120, verbose_name="meno", unique=True)
    info_url = models.URLField()
    points = models.PositiveIntegerField(verbose_name="body", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    chosen_attribute_values = models.ManyToManyField(AttributeValue, blank=True)
    is_protected = models.BooleanField(default=False, editable=False)
    is_published = models.BooleanField(default=False, null=False)
    email_recipients = SeparatedValuesField(verbose_name="príjemcovia", field=models.EmailField)

    pubkey = models.TextField(max_length=1024)
    privkey = models.BinaryField(max_length=4096)
    backup_privkey = models.ForeignKey(BackupKey, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def serialize(self) -> Mapping:
        return model_to_dict(self, fields=["name", "points", "info_url"])

    def change_password(self, old_raw_password, new_raw_password):
        _, encrypted_key = self.get_keypair()
        try:
            private_key = RSA.import_key(encrypted_key, old_raw_password if self.is_protected else "unprotected")
        except (ValueError, IndexError, TypeError):
            raise exceptions.PermissionDenied("invalid current password")
        encrypted_key = export_privkey(private_key, new_raw_password)

        self.privkey = encrypted_key
        self.save()

    def get_keypair(self) -> (bytes, bytes):
        """
        Retrieves the keypair for this user.
        :return: a tuple of the exported public key and the exported private key
        """

        return self.pubkey, self.privkey


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

    def serialize(self) -> Mapping:
        d = model_to_dict(self)
        d["when"] = self.when.isoformat(timespec="minutes")
        return d


class EncryptedToken(models.Model):
    __AES_KEY_LENGTH = 16
    session_keys = SeparatedBinaryField()
    nonce = models.BinaryField()
    tag = models.BinaryField()
    ciphertext = models.BinaryField()

    @classmethod
    def new(cls, token: str, pubkeys: Sequence[RsaKey]) -> Self:
        token_bytes = token.encode("UTF-8")
        enc_keys: list[bytes] = []
        for pubkey in pubkeys:
            cipher_rsa = PKCS1_OAEP.new(pubkey)
            enc_keys.append(cipher_rsa.encrypt(token_bytes))

        return cls(
            session_keys=enc_keys,
            nonce=b"",
            tag=b"",
            ciphertext=b"",
        )

    def _old_decrypt(self, private_key: RsaKey) -> Optional[str]:
        cipher_rsa = PKCS1_OAEP.new(private_key)
        for enc_key in self.session_keys:
            try:
                session_key = cipher_rsa.decrypt(enc_key)
            except ValueError:
                continue
            if len(session_key) != self.__AES_KEY_LENGTH:  # anything else means decryption failed
                continue
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce=self.nonce)
            try:
                token_data = cipher_aes.decrypt_and_verify(self.ciphertext, self.tag)
            except ValueError:
                continue
            token = token_data.decode("utf-8")

            del session_key  # the session key is sensitive, so delete it immediately
            return token
        return None

    def decrypt(self, private_key: RsaKey) -> Optional[str]:
        if self.tag:
            return self._old_decrypt(private_key)

        cipher_rsa = PKCS1_OAEP.new(private_key)
        for enc_token in self.session_keys:
            try:
                token_bytes = cipher_rsa.decrypt(enc_token)
            except ValueError:
                continue
            return token_bytes.decode("UTF-8")


class Participation(models.Model):
    nanoid = models.CharField(max_length=20, unique=True, editable=False, default=generate_nanoid)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False, blank=True, null=False)
    encrypted_token = models.OneToOneField(EncryptedToken, on_delete=models.CASCADE, blank=True, null=True)
