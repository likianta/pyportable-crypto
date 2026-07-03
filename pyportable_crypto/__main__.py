import typing as t
from secrets import token_urlsafe

from argsense import cli
from lk_utils import fs
from neoprint import print

from . import compilation
from . import encryption
from . import keygen
from .cipher_gen import generate_cipher_package


@cli
def encrypt_text(
    text: str, key: t.Optional[str] = None, salty: bool = False
) -> None:
    """
    params:
        key (-k): if not given, will generate a random key.
        salty (-s): if True, will add salt to the key.
    """
    if key is None:
        key = token_urlsafe()
        print('random generated key: {}'.format(key))
    elif salty:
        key = encryption.add_salt(key)
        print('key with salt: {}'.format(key))
    print(encryption.encrypt(data=text, key=key).decode('utf-8'))


@cli
def encrypt_file(
    file_i: str, file_o: str, key: t.Optional[str] = None, salty: bool = False
) -> None:
    if key is None:
        key = token_urlsafe()
        print('random generated key: {}'.format(key))
    elif salty:
        key = encryption.add_salt(key)
        print('key with salt: {}'.format(key))
    encryption.encrypt(file_i=file_i, file_o=file_o, key=key)


@cli
def decrypt_text(encrypted: str, key: str) -> None:
    print(
        ':s1',
        encryption.decrypt(data=encrypted.encode('utf-8'), key=key).decode(
            'utf-8'
        ),
    )


@cli
def decrypt_file(file_i: str, file_o: str, key: str) -> None:
    encryption.decrypt(file_i=file_i, file_o=file_o, key=key)


@cli
def generate_runtime_package(dir_o: str, key: str) -> None:
    """
    create "pyportable_runtime" package under `dir_o`.
    """
    generate_cipher_package(key, dir_o=dir_o)


cli.add_cmd(compilation.compile_module)


@cli
def compile_package(
    dir_i: str,
    dir_o: str,
    key: t.Optional[str] = None,
    salty: bool = False,
    add_runtime_package: str = 'inside',
) -> None:
    """
    params:
        salty (-s):
    """
    if key is None:
        key = keygen.random_key()
    elif salty:
        key = encryption.add_salt(key)
    print(key, ':nv2')

    if fs.exist(dir_o):
        if fs.basename(dir_o) != fs.basename(dir_i):
            dir_o += '/' + fs.basename(dir_i)

    compilation.compile_package(
        dir_i=dir_i,
        dir_o=dir_o,
        key=key,
        add_runtime_package=add_runtime_package,
    )
    print('compiled to "{}"'.format(fs.normpath(dir_o)))


if __name__ == '__main__':
    # python -m pyportable_crypto -h
    # python -m pyportable_crypto compile-dir -h
    cli.run()
