import typing as t
from hashlib import sha256

from ._io import dump_file
from ._io import load_file
from ._pyaes_snippet import AESModeOfOperationCBC
from .formatter import T as T0
from .formatter import formatters


class T(T0):
    FileMode = t.Literal['r', 'rb']
    InData = bytes
    OutData = t.Union[str, bytes]
    OutDataType = t.Literal['str', 'bin']


def decrypt(
        data: bytes = None,
        key: str = None,
        *,
        from_file: str = None,
        from_file_mode: T.FileMode = 'rb',
        to_file: str = None,
        to_file_mode: T.FileMode = 'wb',
) -> T.OutData:
    assert key
    if not data:
        assert from_file and from_file_mode
        data = load_file(from_file, from_file_mode)
    # noinspection PyTypeChecker
    out = decrypt_data(data, key, 'bin' if to_file_mode[-1] == 'b' else 'str')
    if to_file:
        dump_file(out, to_file, to_file_mode)
    return out


def decrypt_data(
        enc_data: bytes,
        key: str,
        type_o: T.OutDataType = 'str',
        size: int = 16,
        fmt: T.FormatterName = 'base64',
) -> T.OutData:
    _enc_data = formatters[fmt].decode(enc_data)  # type: bytes
    _key = sha256(key.encode('utf-8')).digest()  # type: bytes
    
    cipher = AESModeOfOperationCBC(_key)
    
    # # _dec_data = _unpad(cipher.decrypt(_enc_data))  # type: bytes
    _dec_data = b''
    for i in range(0, len(_enc_data), size):
        _dec_data += cipher.decrypt(_enc_data[i:i + size])
    dec_data = _unpad(_dec_data)  # type: bytes
    
    if type_o == 'str':
        return dec_data.decode('utf-8')
    else:
        return dec_data


def _unpad(s: bytes) -> bytes:
    return s[:-ord(s[len(s) - 1:])]
