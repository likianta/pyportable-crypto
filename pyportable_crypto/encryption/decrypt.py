import typing as t
from hashlib import sha256

from lk_utils import fs

from ._pyaes_snippet import AESModeOfOperationCBC
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


def decrypt_file(
    file_i: str, file_o: t.Optional[str] = None, *, key: str
) -> t.Optional[bytes]:
    with open(file_i, 'rb') as f:
        dec = decrypt_data(f.read(), key)
    if file_o:
        with open(file_o, 'wb') as f:
            f.write(dec)
    else:
        return dec


def decrypt_data(
    data: bytes, key: str, size: int = 16, fmt: str = 'base64'
) -> bytes:
    datax = formatters[fmt].decode(data)  # type: bytes
    keyx = sha256(key.encode('utf-8')).digest()  # type: bytes

    cipher = AESModeOfOperationCBC(keyx)

    decx = b''
    for i in range(0, len(datax), size):
        decx += cipher.decrypt(datax[i : i + size])
    dec = _unpad(decx)  # type: bytes
    return dec


def _unpad(s: bytes) -> bytes:
    return s[: -ord(s[len(s) - 1 :])]
