from hashlib import sha256

from ._pyaes_snippet import AESModeOfOperationCBC
from .formatter import formatters


def decrypt_file(file_i, file_o=None, key=None) -> str:
    if not key:
        raise Exception
    with open(file_i, 'rb') as f:
        enc_data = f.read()
    dec_data = decrypt_data(enc_data, key)
    if file_o:
        with open(file_o, 'w', encoding='utf-8') as f:
            f.write(dec_data)
    return dec_data


def decrypt_data(enc_data: bytes, key: str, size=16, fmt='base64') -> str:
    _enc_data = formatters[fmt].decode(enc_data)  # type: bytes
    _key = sha256(key.encode('utf-8')).digest()  # type: bytes
    
    cipher = AESModeOfOperationCBC(_key)
    
    # # _dec_data = _unpad(cipher.decrypt(_enc_data))  # type: bytes
    _dec_data = b''
    for i in range(0, len(_enc_data), size):
        _dec_data += cipher.decrypt(_enc_data[i:i + size])
    dec_data = _unpad(_dec_data).decode('utf-8')  # type: str
    return dec_data


def _unpad(s: bytes) -> bytes:
    return s[:-ord(s[len(s) - 1:])]
