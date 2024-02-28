from pathlib import Path

from Crypto.PublicKey.RSA import RsaKey
from django.conf import settings
from django.utils.text import slugify


def export_privkey(key: RsaKey, passphrase: str) -> bytes:
    return key.export_key(passphrase=passphrase, pkcs=8, format="DER",
                          protection="PBKDF2WithHMAC-SHA1AndAES256-CBC")


def get_keydir(name: str) -> Path:
    slug = slugify(name)
    return settings.BASE_DIR / "keys" / "research" / slug[0] / slug
