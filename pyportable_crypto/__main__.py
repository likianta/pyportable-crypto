import typing as t
from secrets import token_urlsafe

from argsense import cli

from .cipher_gen import generate_cipher_package
from .compilation import compile_module
from .compilation import compile_package
from .encryption import decrypt
from .encryption import encrypt


@cli
def encrypt_text(text: str, key: t.Optional[str] = None) -> None:
    """
    params:
        key: if not given, will generate a random key.
    """
    if key is None:
        key = token_urlsafe()
        print('random generated key: {}'.format(key), ':s1')
    print(encrypt(data=text, key=key).decode('utf-8'), ':s1')


@cli
def encrypt_file(file_i: str, file_o: str, key: str) -> None:
    encrypt(file_i=file_i, file_o=file_o, key=key)


@cli
def decrypt_text(encrypted: str, key: str) -> None:
    print(
        ':s1', decrypt(data=encrypted.encode('utf-8'), key=key).decode('utf-8')
    )


@cli
def decrypt_file(file_i: str, file_o: str, key: str) -> None:
    decrypt(file_i=file_i, file_o=file_o, key=key)


@cli
def generate_runtime_package(dir_o: str, key: str) -> None:
    """
    create "pyportable_runtime" package under `dir_o`.
    """
    generate_cipher_package(key, dir_o=dir_o)


cli.add_cmd(compile_module)
cli.add_cmd(compile_package)


if __name__ == '__main__':
    # python -m pyportable_crypto -h
    # python -m pyportable_crypto compile-dir -h
    cli.run()
