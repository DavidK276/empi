from io import BytesIO
from pathlib import Path

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Random import get_random_bytes
from django.conf import settings
from django.utils.text import slugify


def export_privkey(key: RsaKey, passphrase: str) -> bytes:
    return key.export_key(passphrase=passphrase, pkcs=8, format="DER",
                          protection="PBKDF2WithHMAC-SHA1AndAES256-CBC")


def get_keydir(name: str) -> Path:
    slug = slugify(name)
    return settings.BASE_DIR / "keys" / "research" / slug[0] / slug


def encrypt_token(token: str, pubkey: RsaKey):
    session_key = get_random_bytes(16)
    cipher_rsa = PKCS1_OAEP.new(pubkey)
    enc_session_key = cipher_rsa.encrypt(session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(token.encode('utf-8'))

    return enc_session_key + cipher_aes.nonce + tag + ciphertext


def parse_encrypted_data(data: bytes, privkey_size: int):
    f = BytesIO(data)
    enc_session_key = f.read(privkey_size)
    nonce = f.read(16)
    tag = f.read(16)
    ciphertext = f.read()
    return enc_session_key, nonce, tag, ciphertext
