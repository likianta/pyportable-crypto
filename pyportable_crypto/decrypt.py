from base64 import b64decode
from hashlib import sha256

from Cryptodome.Cipher import AES


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


def decrypt_data(enc_data: bytes, key: str) -> str:
    _enc_data = b64decode(enc_data)  # type: bytes
    key = sha256(key.encode('utf-8')).digest()  # type: bytes
    iv = _enc_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    _dec_data = _unpad(cipher.decrypt(_enc_data[AES.block_size:]))  # type: bytes
    dec_data = _dec_data.decode('utf-8')  # type: str
    return dec_data


def _unpad(s: bytes) -> bytes:
    return s[:-ord(s[len(s) - 1:])]
