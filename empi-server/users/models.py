import datetime
import random
from collections.abc import Mapping, Sequence, Iterable
from typing import Self

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from nanoid import generate
from rest_framework import exceptions

from utils.keys import export_privkey, export_privkey_plaintext


class EmpiUserManager(UserManager):

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

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super().get_queryset().defer("pubkey", "privkey", "backup_privkey")

    def create_superuser(self, email=None, password=None, **extra_fields):
        if password is not None:
            extra_fields |= self.init_keys(password)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        if password is not None:
            extra_fields |= self.init_keys(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


class EncryptedSessionKey(models.Model):
    admin = models.ForeignKey("EmpiUser", on_delete=models.CASCADE, related_name="user_esk_admin")
    backup_key = models.ForeignKey("BackupKey", on_delete=models.CASCADE)

    data = models.BinaryField(max_length=1024)


class BackupKey(models.Model):
    nonce = models.BinaryField(max_length=16)
    tag = models.BinaryField(max_length=16)
    backup_key = models.BinaryField(max_length=4096)


class ResetKey(models.Model):
    user = models.OneToOneField("EmpiUser", on_delete=models.CASCADE)
    valid_until = models.DateTimeField()
    backup_key = models.BinaryField(max_length=4096)

    @classmethod
    def new(cls, user, backup_key: bytes):
        try:
            ResetKey.objects.get(user=user.pk).delete()
        except ResetKey.DoesNotExist:
            pass
        valid_until = timezone.now() + datetime.timedelta(hours=24)
        return cls(user=user, valid_until=valid_until, backup_key=backup_key)


class EmpiUser(AbstractBaseUser, PermissionsMixin):
    users = EmpiUserManager()

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    pubkey = models.BinaryField(max_length=1024)
    privkey = models.BinaryField(max_length=4096)
    backup_privkey = models.ForeignKey(BackupKey, on_delete=models.CASCADE)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        default_manager_name = "users"

    def get_keypair(self) -> (bytes, bytes):
        """
        Retrieves the keypair for this user.
        :return: a tuple of the exported public key and the exported private key
        """

        return self.pubkey, self.privkey

    def change_password(self, old_raw_password, new_raw_password):
        if self.has_usable_password():
            if not self.check_password(old_raw_password):
                raise exceptions.PermissionDenied("invalid password")
        self.set_password(new_raw_password)

        _, encrypted_key = self.get_keypair()
        private_key = RSA.import_key(encrypted_key, old_raw_password)
        encrypted_key = export_privkey(private_key, new_raw_password)

        self.privkey = encrypted_key
        self.save()

    def use_backup_key(self, admin: Self, admin_password: str) -> RsaKey:
        try:
            admin_key = EncryptedSessionKey.objects.get(admin=admin.pk, backup_key=self.backup_privkey.pk)
        except EncryptedSessionKey.DoesNotExist:
            raise exceptions.PermissionDenied("This admin has not protected this user")

        _, enc_privkey = admin.get_keypair()
        admin_privkey = RSA.import_key(enc_privkey, admin_password)
        cipher_rsa = PKCS1_OAEP.new(admin_privkey)

        sessionkey = cipher_rsa.decrypt(admin_key.data)

        cipher_aes = AES.new(sessionkey, AES.MODE_EAX, nonce=self.backup_privkey.nonce)
        return RSA.import_key(cipher_aes.decrypt_and_verify(self.backup_privkey.backup_key, self.backup_privkey.tag))

    def change_password_admin(self, admin: Self, admin_password: str, new_password: str):
        decrypted_user_privkey = self.use_backup_key(admin, admin_password)

        self.privkey = export_privkey(decrypted_user_privkey, new_password)
        self.set_password(new_password)
        self.save()

    def make_reset_key(self, admin: Self, admin_password: str):
        decrypted_user_privkey = self.use_backup_key(admin, admin_password)
        passphrase = generate(alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", size=64)

        reset_key = ResetKey.new(self, export_privkey(decrypted_user_privkey, passphrase))
        reset_key.save()

        return passphrase

    def reset_password(self, reset_key: ResetKey, passphrase: str, new_password: str):
        try:
            privkey = RSA.import_key(reset_key.backup_key, passphrase)
        except (ValueError, IndexError, TypeError):
            return False
        self.privkey = export_privkey(privkey, new_password)
        self.set_password(new_password)
        self.save()

    def is_participant(self):
        return Participant.objects.filter(user=self.pk).exists()


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
        try:
            return "%s > %s" % (str(self.attribute), self.value)
        except AttributeValue.attribute.RelatedObjectDoesNotExist:
            return self.value

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
    now = timezone.now()
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
