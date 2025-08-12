from argsense import cli

from .cipher_gen import generate_cipher_package
from .compilation import compile_dir
from .compilation import compile_file
from .encryption import decrypt_data
from .encryption import encrypt_data


@cli
def encrypt_text(text: str, key: str = None):
    """
    params:
        key: if not given, will generate a random key.
    """
    if key is None:
        from secrets import token_urlsafe
        key = token_urlsafe()
        print('random generated key: {}'.format(key), ':s1')
    print(encrypt_data(text, key).decode('utf-8'), ':s1v1')


@cli
def decrypt_text(encrypted: str, key: str) -> None:
    print(':s1v2', decrypt_data(encrypted.encode('utf-8'), key).decode('utf-8'))


@cli
def generate_runtime_package(dir_o: str, key: str) -> None:
    generate_cipher_package(dir_o, key)


cli.add_cmd(compile_file)
cli.add_cmd(compile_dir)


@cli
def deploy_compiled_binary(dir_o: str, key: str) -> None:
    from .cipher_gen import generate_cipher_package
    generate_cipher_package(dir_o, key)


if __name__ == '__main__':
    # py -m pyportable_crypto -h
    # py -m pyportable_crypto compile-dir -h
    cli.run()
