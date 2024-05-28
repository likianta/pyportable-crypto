from argsense import cli

from . import __version__
from .compilation import compile_dir
from .compilation import compile_file
from .encryption import encrypt_data

print(__version__)


@cli.cmd()
def encrypt_text(text: str, key: str = None):
    """
    kwargs:
        key: if not given, will generate a random key.
    """
    if key is None:
        from secrets import token_urlsafe
        key = token_urlsafe()
    print(key)
    print('\n' + str(encrypt_data(text, key)), ':s')


cli.add_cmd(compile_file)
cli.add_cmd(compile_dir)


@cli.cmd()
def deploy_compiled_binary(dir_o: str, key: str) -> None:
    from .cipher_gen import generate_cipher_package
    generate_cipher_package(dir_o, key)


if __name__ == '__main__':
    # py -m pyportable_crypto -h
    # py -m pyportable_crypto compile-dir -h
    cli.run()
