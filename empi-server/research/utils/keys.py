from io import BytesIO
from pathlib import Path

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from django.conf import settings
from django.utils.text import slugify


def export_privkey(key: RsaKey, passphrase: str) -> bytes:
    return key.export_key(
        passphrase=passphrase,
        pkcs=8,
        format="DER",
        protection="PBKDF2WithHMAC-SHA1AndAES256-CBC",
    )


def get_keydir(name: str) -> Path:
    slug = slugify(name)
    return settings.BASE_DIR / "keys" / "research" / slug[0] / slug
