from hashlib import sha256

from ._pyaes_snippet import AESModeOfOperationCBC
from .formatter import formatters


def encrypt_file(file_i, file_o, key: str):
    with open(file_i, 'r', encoding='utf-8') as r:
        data = r.read()
    with open(file_o, 'wb') as w:
        w.write(encrypt_data(data, key))
    return file_o


def encrypt_data(data: str, key: str, size=16, fmt='base64') -> bytes:
    _data = _pad(data).encode('utf-8')  # type: bytes
    _key = sha256(key.encode('utf-8')).digest()  # type: bytes
    
    cipher = AESModeOfOperationCBC(_key)
    
    # # _enc_data = cipher.encrypt(_data)  # type: bytes
    _enc_data = b''
    for i in range(0, len(_data), size):
        _enc_data += cipher.encrypt(_data[i:i + size])
    enc_data = formatters[fmt].encode(_enc_data)  # type: bytes
    return enc_data


def _pad(s: str, size=16) -> str:
    # sometimes len(s) doesn't equal to len(s.encode()), we should use bytes
    # length here.
    bytelen = len(s.encode('utf-8'))
    return s + (size - bytelen % size) * chr(size - bytelen % size)
