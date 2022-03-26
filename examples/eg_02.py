from lk_utils import dumps
from lk_utils import loads

from pyportable_crypto import decrypt_data
from pyportable_crypto import encrypt_data

key = 'abcd123'

file_i = input('file to encrypt: ')
file_o1 = file_i.rsplit('.', 1)[0] + '.enc.txt'
file_o2 = file_i.rsplit('.', 1)[0] + '.dec.txt'

plain_text = loads(file_i)
encrypted_text = encrypt_data(plain_text, key)
# print(f'{encrypted_text = }')
dumps(str(encrypted_text), file_o1)

plain_text = decrypt_data(encrypted_text, key)
# print(f'{plain_text = }')
dumps(plain_text, file_o2)
