import os

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from neoprint import print

key = ChaCha20Poly1305.generate_key()
print(key, ':n')
chacha = ChaCha20Poly1305(key)

nonce = os.urandom(12)

ciphertext = chacha.encrypt(nonce, b'hello world', None)

plaintext = chacha.decrypt(nonce, ciphertext, None)

print('plaintext', plaintext.decode())
