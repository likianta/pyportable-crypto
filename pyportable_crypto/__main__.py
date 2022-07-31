import os

try:
    from argsense import cli
except Exception:
    print('Command line tool is not installed! Please install it by pip: \n'
          '\tpip install argsense')
    exit(-1)

from .compiler import Compiler


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
