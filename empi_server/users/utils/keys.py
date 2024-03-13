from pathlib import Path
from typing import Optional

from Crypto.PublicKey.RSA import RsaKey
from django.conf import settings


def export_privkey(key: RsaKey, passphrase: str) -> bytes:
    return key.export_key(
        passphrase=passphrase,
        pkcs=8,
        format="DER",
        protection="PBKDF2WithHMAC-SHA1AndAES256-CBC",
    )


def get_keydir(username: str) -> Optional[Path]:
    if not username:
        return None
    return settings.BASE_DIR / "keys" / "users" / username[0] / username
