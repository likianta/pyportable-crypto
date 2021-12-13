"""
References:
    https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto
        -aes-256
    https://blog.csdn.net/Flower941220/article/details/101166912
    
Warnings:
    docs/cythonize-known-issues.zh.md
"""
from . import keygen
from .decrypt import decrypt_data
from .decrypt import decrypt_file
from .encrypt import encrypt_data
from .encrypt import encrypt_file

__version__ = '0.3.0'
