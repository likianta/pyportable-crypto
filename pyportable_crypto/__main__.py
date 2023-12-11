import os

from argsense import cli

from . import __version__
from .compiler import PyCompiler
from .encrypt import encrypt_data

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


@cli.cmd()
def compile_file(file_i: str, file_o: str, key: str):
    """
    args:
        file_i: the file should be a '.py' file.
        file_o: use the same extension name ('.py') as `file_i`.
    """
    compiler = PyCompiler(key, os.path.dirname(file_o))
    compiler.compile_file(file_i, file_o)


@cli.cmd()
def compile_dir(
    dir_i: str, dir_o: str, key: str, reuse_runtime: bool = False
) -> None:
    """
    iterate all ".py" files in `dir_i` and compile them to `dir_o`.
    """
    compiler = PyCompiler(
        key,
        dir_o,
        reuse_runtime=reuse_runtime,
        overwrite_runtime=True,
    )
    compiler.compile_dir(dir_i, dir_o)


# -----------------------------------------------------------------------------


@cli.cmd()
def deploy_compiled_binary(dir_o: str, key: str) -> None:
    from .cipher_gen import generate_cipher_package
    generate_cipher_package(dir_o, key)


if __name__ == '__main__':
    # py -m pyportable_crypto -h
    # py -m pyportable_crypto compile-dir -h
    cli.run()
