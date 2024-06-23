from Crypto.PublicKey.RSA import RsaKey


def export_privkey(key: RsaKey, passphrase: str) -> bytes:
    return key.export_key(
        passphrase=passphrase,
        pkcs=8,
        format="DER",
        protection="PBKDF2WithHMAC-SHA1AndAES256-CBC",
    )


def export_privkey_plaintext(key: RsaKey) -> bytes:
    return key.export_key(passphrase=None, pkcs=1, format="DER")
