import typing as t
from hashlib import sha256

from ._io import dump_file
from ._io import load_file
from ._pyaes_snippet import AESModeOfOperationCBC
from .formatter import T as T0
from .formatter import formatters


class T(T0):
    FileMode = t.Literal['r', 'rb']
    InData = t.Union[str, bytes]
    OutData = bytes


def encrypt(
        data: T.InData = None,
        key: str = None,
        *,
        from_file: str = None,
        from_file_mode: T.FileMode = 'rb',
        to_file: str = None,
        to_file_mode: T.FileMode = 'wb',
        size: int = 16,
        fmt: T.FormatterName = 'base64',
) -> T.OutData:
    assert key
    if not data:
        assert from_file
        data = load_file(from_file, from_file_mode)
    out = encrypt_data(data, key, size, fmt)
    if to_file:
        assert to_file_mode == 'wb'
        dump_file(out, to_file, 'wb')
    return out


def encrypt_data(
        data: T.InData,
        key: str,
        size: int = 16,
        fmt: T.FormatterName = 'base64',
) -> T.OutData:
    _data = _pad(data if isinstance(data, bytes)
                 else data.encode('utf-8'))  # type: bytes
    _key = sha256(key.encode('utf-8')).digest()  # type: bytes
    
    cipher = AESModeOfOperationCBC(_key)
    
    # # _enc_data = cipher.encrypt(_data)  # type: bytes
    _enc_data = b''
    for i in range(0, len(_data), size):
        _enc_data += cipher.encrypt(_data[i:i + size])
    enc_data = formatters[fmt].encode(_enc_data)  # type: bytes
    return enc_data


def _pad(s: bytes, size: int = 16) -> bytes:
    return s + (
            (size - len(s) % size)
            * chr(size - len(s) % size)
    ).encode('utf-8')
