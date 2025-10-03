import warnings
from collections.abc import Sequence, Mapping
from datetime import timedelta
from typing import Self, Optional

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, Manager
from django.forms import model_to_dict
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions

from empi_server.fields import SeparatedValuesField
from empi_settings.models import Settings
from users.models import EmpiUser, AttributeValue
from utils.keys import export_privkey, export_privkey_plaintext
from .fields import SeparatedBinaryField
from .utils.constants import *
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
                admin=admin, backup_key=backup_privkey, data=cipher_rsa.encrypt(session_key)
            )
            enc_session_key.save()
        return {"privkey": privkey, "pubkey": pubkey, "backup_privkey": backup_privkey}

    def get_queryset(self):
        return super().get_queryset().defer("pubkey", "privkey", "backup_privkey")

    def create(self, **kwargs):
        return super().create(**(kwargs | self.init_keys("unprotected")))


class EncryptedSessionKey(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="research_esk_admin")
    backup_key = models.ForeignKey("BackupKey", on_delete=models.CASCADE)

    data = models.BinaryField(max_length=1024)


class BackupKey(models.Model):
    nonce = models.BinaryField(max_length=16)
    tag = models.BinaryField(max_length=16)
    backup_key = models.BinaryField(max_length=4096)

    def __str__(self):
        return "%s BackupKey"


class ResetKey(models.Model):
    user = models.OneToOneField("Research", on_delete=models.CASCADE)
    valid_until = models.DateTimeField()
    backup_key = models.BinaryField(max_length=4096)

    @classmethod
    def new(cls, user, backup_key: bytes):
        try:
            ResetKey.objects.get(user=user.pk).delete()
        except ResetKey.DoesNotExist:
            pass
        valid_until = timezone.now() + timedelta(hours=24)
        return cls(valid_until=valid_until, backup_key=backup_key)


class Research(models.Model):
    objects = ResearchManager()

    nanoid = models.CharField(max_length=20, unique=True, editable=False, default=generate_nanoid)
    name = models.CharField(max_length=120, verbose_name="meno", unique=True)
    comment = models.TextField(blank=True)
    info_url = models.URLField(blank=True, null=True, max_length=500)
    points = models.PositiveIntegerField(verbose_name="body", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    chosen_attribute_values = models.ManyToManyField(AttributeValue, blank=True)
    is_protected = models.BooleanField(default=False, editable=False)
    is_published = models.BooleanField(default=False, null=False)
    email_recipients = SeparatedValuesField(verbose_name="príjemcovia", field=models.EmailField)

    pubkey = models.BinaryField(max_length=1024)
    privkey = models.BinaryField(max_length=4096)
    backup_privkey = models.ForeignKey(BackupKey, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def serialize(self) -> Mapping:
        return model_to_dict(self, fields=["name", "points", "info_url"])

    def change_password(self, old_raw_password, new_raw_password):
        try:
            private_key = RSA.import_key(self.privkey, old_raw_password if self.is_protected else "unprotected")
        except (ValueError, IndexError, TypeError):
            raise exceptions.PermissionDenied(_("invalid current password"))
        encrypted_key = export_privkey(private_key, new_raw_password)

        self.privkey = encrypted_key
        self.is_protected = new_raw_password != "unprotected"
        self.save(update_fields=["privkey", "is_protected"])

    @property
    def has_open_appointments(self) -> bool:
        return Appointment.objects.all().filter(Q(research=self) & Q(when__gt=timezone.now())).exists()


class Appointment(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    when = models.DateTimeField(verbose_name="kedy", blank=True, null=True)
    capacity = models.IntegerField(verbose_name="kapacita")
    comment = models.TextField(blank=True)
    location = models.TextField(blank=False, null=True)
    info_url = models.URLField(blank=False, null=True, max_length=500)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(info_url__isnull=True) ^ Q(location__isnull=True),
                name="one_of_url_location_null",
            )
        ]

    def __str__(self):
        return f"{self.research.name} / {self.when.strftime('%d. %m. %Y, %H:%M')} ({self.pk})"

    def get_type(self):
        if self.location is None:
            return AppointmentType.ONLINE
        return AppointmentType.IN_PERSON

    def get_pubkeys(self, user) -> Sequence[RsaKey]:
        pubkeys = [RSA.import_key(self.research.pubkey), RSA.import_key(user.pubkey)]

        admins = get_user_model().users.filter(is_staff=True)
        for admin in admins:
            pubkeys.append(RSA.import_key(admin.pubkey))
        return pubkeys

    @property
    def free_capacity(self) -> int:
        return self.capacity - Participation.objects.filter(appointment=self).count()

    def serialize(self) -> Mapping:
        d = model_to_dict(self)
        d["when"] = self.when.strftime("%d. %m. %Y %H:%M")
        return d


class Participation(models.Model):
    SEMESTER_CHOICES = (("Z", "Zimný"), ("L", "Letný"))
    nanoid = models.CharField(max_length=20, unique=True, editable=False, default=generate_nanoid)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False, blank=True, null=False)
    encrypted_tokens = SeparatedBinaryField(blank=True, null=True)
    academic_year = models.CharField(editable=False, default="2024/2025", max_length=15)
    semester = models.CharField(max_length=1, editable=False, choices=SEMESTER_CHOICES, default="Z")
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.appointment.research.name} / {self.appointment.when.strftime('%d. %m. %Y, %H:%M')} ({self.pk})"

    @classmethod
    def new(
        cls,
        token: str,
        appointment: Appointment,
        is_confirmed: bool,
        pubkeys: Sequence[RsaKey],
    ) -> Self:
        token_bytes = token.encode("UTF-8")
        encrypted_tokens: list[bytes] = []
        for pubkey in pubkeys:
            cipher_rsa = PKCS1_OAEP.new(pubkey)
            encrypted_tokens.append(cipher_rsa.encrypt(token_bytes))

        current_acad_year, current_semester = cls.get_current_semester()
        return cls(
            appointment=appointment,
            is_confirmed=is_confirmed,
            encrypted_tokens=encrypted_tokens,
            academic_year=current_acad_year,
            semester=current_semester,
        )

    def add_encrypted_token(self, token: str, pubkey: RsaKey):
        cipher_rsa = PKCS1_OAEP.new(pubkey)
        self.encrypted_tokens.append(cipher_rsa.encrypt(token.encode("UTF-8")))

    def decrypt(self, private_key: RsaKey) -> Optional[str]:
        if not self.encrypted_tokens:
            warnings.warn(f"Participation {{{self}}} seems to have no participants? This is not right.")
            return None
        cipher_rsa = PKCS1_OAEP.new(private_key)
        for enc_token in self.encrypted_tokens:
            try:
                token_bytes = cipher_rsa.decrypt(enc_token)
                return token_bytes.decode("UTF-8")
            except ValueError:
                continue
            except UnicodeDecodeError:
                continue
        return None

    @staticmethod
    def get_current_semester():
        try:
            acad_year_setting = Settings.objects.get(name="CURRENT_ACAD_YEAR").value
            semester_setting = Settings.objects.get(name="CURRENT_SEMESTER").value
            return acad_year_setting, semester_setting
        except Settings.DoesNotExist:
            now = timezone.now()
            if now.month >= 7:
                return f"{now.year}/{now.year + 1}", "Z"
            return f"{now.year - 1}/{now.year}", "Z"
