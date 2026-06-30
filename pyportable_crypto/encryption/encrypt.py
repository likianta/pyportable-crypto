import os
import typing as t
from hashlib import sha256

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from lk_utils import fs

from .formatter import formatters


def encrypt(
    *,
    data: t.Optional[t.Union[str, bytes]] = None,
    data_i: t.Optional[t.Union[str, bytes]] = None,
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

    data_dec = data_i if data_i else fs.load(t.cast(str, file_i), 'binary')
    data_enc = encrypt_data(data_dec, key)
    if file_o:
        fs.dump(data_enc, file_o, 'binary')
    return data_enc


def encrypt_data(
    data: t.Union[str, bytes], key: str, fmt: str = 'base64'
) -> bytes:
    """
    https://share.gemini.google/sBT8jVKFDnxu
    """
    keyx = sha256(key.encode('utf-8')).digest()
    chacha = ChaCha20Poly1305(keyx)
    nonce = os.urandom(12)

    plain_data = data if isinstance(data, bytes) else data.encode('utf-8')
    cipher_data = chacha.encrypt(nonce, plain_data, None)
    return formatters[fmt].encode(nonce + cipher_data)


# DELETE
def _pad(s: bytes, size: int = 16) -> bytes:
    return s + ((size - len(s) % size) * chr(size - len(s) % size)).encode(
        'utf-8'
    )
