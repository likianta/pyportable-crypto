"""
References:
    https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto
        -aes-256
    https://blog.csdn.net/Flower941220/article/details/101166912
    
Warnings:
    docs/cythonize-known-issues.zh.md
"""
import lk_logger
lk_logger.setup(quiet=True, show_varnames=True)

from . import cipher_gen
from . import keygen
from .compiler import PyCompiler
from .decrypt import decrypt_data
from .decrypt import decrypt_file
from .encrypt import encrypt_data
from .encrypt import encrypt_file

__version__ = '1.0.3'
