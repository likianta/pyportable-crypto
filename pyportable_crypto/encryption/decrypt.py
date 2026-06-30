import typing as t
from hashlib import sha256

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from lk_utils import fs

from .formatter import formatters


def decrypt(
    *,
    data: t.Optional[bytes] = None,
    data_i: t.Optional[bytes] = None,
    file: t.Optional[str] = None,
    file_i: t.Optional[str] = None,
    file_o: t.Optional[str] = None,
    key: str,
) -> bytes:
    # distinguish data io and file io
    if data and file:
        data_i = data
        file_o = file
    # del data
    if not data_i and file:
        file_i = file
    # del file

    data_enc = data_i if data_i else fs.load(t.cast(str, file_i), 'binary')
    data_dec = decrypt_data(data_enc, key)
    if file_o:
        fs.dump(data_dec, file_o, 'binary')
    return data_dec


def decrypt_data(data: bytes, key: str, fmt: str = 'base64') -> bytes:
    """
    https://share.gemini.google/sBT8jVKFDnxu
    """
    keyx = sha256(key.encode('utf-8')).digest()
    chacha = ChaCha20Poly1305(keyx)
    cipher_b64 = data
    cipher_bytes = formatters[fmt].decode(cipher_b64)
    nonce = cipher_bytes[:12]
    cipher_data = cipher_bytes[12:]
    plain_data = chacha.decrypt(nonce, cipher_data, None)
    return plain_data


# DELETE
def _unpad(s: bytes) -> bytes:
    return s[: -ord(s[len(s) - 1 :])]
