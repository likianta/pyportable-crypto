import typing as t
from hashlib import sha256

from lk_utils import fs

from ._pyaes_snippet import AESModeOfOperationCBC
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


def encrypt_file(
    file_i: str, file_o: t.Optional[str] = None, *, key: str
) -> t.Optional[bytes]:
    with open(file_i, 'rb') as f:
        enc = encrypt_data(f.read(), key)
    if file_o:
        with open(file_o, 'wb') as f:
            f.write(enc)
    else:
        return enc


def encrypt_data(
    data: t.Union[str, bytes], key: str, size: int = 16, fmt: str = 'base64'
) -> bytes:
    datax = _pad(  # type: bytes
        data if isinstance(data, bytes) else data.encode('utf-8')
    )
    keyx = sha256(key.encode('utf-8')).digest()  # type: bytes

    cipher = AESModeOfOperationCBC(keyx)

    encx = b''
    for i in range(0, len(datax), size):
        encx += cipher.encrypt(datax[i : i + size])
    enc = formatters[fmt].encode(encx)  # type: bytes
    return enc


def _pad(s: bytes, size: int = 16) -> bytes:
    return s + ((size - len(s) % size) * chr(size - len(s) % size)).encode(
        'utf-8'
    )
