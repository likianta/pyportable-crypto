"""
references:
    https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto
    -aes-256
    https://blog.csdn.net/Flower941220/article/details/101166912

warnings:
    docs/cythonize-known-issues.zh.md
"""

# TODO
# - rename `compile_dir` to `compile_package` or `encrypt_package`
# - rename `compile_file` to `compile_module` or `encrypt_module`

from . import cipher_gen
from .compilation import PyCompiler
from .compilation import compile_dir
from .compilation import compile_file
from .encryption import decrypt
from .encryption import decrypt_data
from .encryption import decrypt_file
from .encryption import encrypt
from .encryption import encrypt_data
from .encryption import encrypt_file
from .encryption import keygen

__version__ = '1.5.2'
