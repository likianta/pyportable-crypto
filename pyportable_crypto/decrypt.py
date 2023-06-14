from hashlib import sha256
from typing import Literal
from typing import Union

from ._pyaes_snippet import AESModeOfOperationCBC
from .formatter import T as T0
from .formatter import formatters


class T:
    FormatterName = T0.FormatterName
    DecryptedData = Union[str, bytes]
    DecryptedDataType = Literal['str', 'bin']


def decrypt_file(
        file_i: str,
        file_o: str = None,
        key: str = None,
        type_o: T.DecryptedDataType = 'str',
) -> T.DecryptedData:
    if not key:
        raise Exception
    with open(file_i, 'rb') as f:
        enc_data = f.read()
    dec_data = decrypt_data(enc_data, key, type_o)
    if file_o:
        if type_o == 'str':
            with open(file_o, 'w', encoding='utf-8') as f:
                f.write(dec_data)
        else:
            with open(file_o, 'wb') as f:
                f.write(dec_data)
    return dec_data


def decrypt_data(
        enc_data: bytes,
        key: str,
        type_o: T.DecryptedDataType = 'str',
        size: int = 16,
        fmt: T.FormatterName = 'base64',
) -> T.DecryptedData:
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
