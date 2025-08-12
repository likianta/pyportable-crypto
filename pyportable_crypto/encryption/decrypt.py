import typing as t
from hashlib import sha256

from ._pyaes_snippet import AESModeOfOperationCBC
from .formatter import formatters


def decrypt_file(
    file_i: str, file_o: str = None, *, key: str
) -> t.Optional[bytes]:
    with open(file_i, 'rb') as f:
        dec = decrypt_data(f.read(), key)
    if file_o:
        with open(file_o, 'wb') as f:
            f.write(dec)
    else:
        return dec


def decrypt_data(
    data: bytes,
    key: str,
    size: int = 16,
    fmt: str = 'base64',
) -> bytes:
    datax = formatters[fmt].decode(data)  # type: bytes
    keyx = sha256(key.encode('utf-8')).digest()  # type: bytes
    
    cipher = AESModeOfOperationCBC(keyx)
    
    decx = b''
    for i in range(0, len(datax), size):
        decx += cipher.decrypt(datax[i:i + size])
    dec = _unpad(decx)  # type: bytes
    return dec


def _unpad(s: bytes) -> bytes:
    return s[:-ord(s[len(s) - 1:])]
