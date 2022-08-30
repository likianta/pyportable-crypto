try:
    from argsense import cli  # noqa
except ImportError:
    print(':v4', 'Command line tool not found!\n'
                 'Please install it with: `pip install argsense`')
    exit(-1)

import os

from . import __version__
from .compiler import Compiler
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
    compiler = Compiler(key, os.path.dirname(file_o))
    compiler.compile_file(file_i, file_o)


@cli.cmd()
def compile_dir(dir_i: str, dir_o: str, key: str):
    compiler = Compiler(key, dir_o)
    compiler.compile_dir(dir_i, dir_o)


if __name__ == '__main__':
    cli.run()
