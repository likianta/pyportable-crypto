from pyportable_crypto import decrypt_data, encrypt_data

key = 'abcd123'
plain_text = 'hello world'

encrypted_text = encrypt_data(plain_text, key)
print(f'{encrypted_text = }')

plain_text = decrypt_data(encrypted_text, key)
print(f'{plain_text = }')
