import typing as t
from hashlib import sha256

from ._pyaes_snippet import AESModeOfOperationCBC
from .formatter import formatters


def encrypt_file(
    file_i: str, file_o: str = None, *, key: str
) -> t.Optional[bytes]:
    with open(file_i, 'rb') as f:
        enc = encrypt_data(f.read(), key)
    if file_o:
        with open(file_o, 'wb') as f:
            f.write(enc)
    else:
        return enc


def encrypt_data(
    dec: t.Union[str, bytes],
    key: str,
    size: int = 16,
    fmt: str = 'base64',
) -> bytes:
    dec2 = _pad(  # type: bytes
        dec if isinstance(dec, bytes)
        else dec.encode('utf-8')
    )
    key2 = sha256(key.encode('utf-8')).digest()  # type: bytes
    
    cipher = AESModeOfOperationCBC(key2)
    
    enc2 = b''
    for i in range(0, len(dec2), size):
        enc2 += cipher.encrypt(dec2[i:i + size])
    enc = formatters[fmt].encode(enc2)  # type: bytes
    return enc


def _pad(s: bytes, size: int = 16) -> bytes:
    return (
        s + ((size - len(s) % size) * chr(size - len(s) % size)).encode('utf-8')
    )
