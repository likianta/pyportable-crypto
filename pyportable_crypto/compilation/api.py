import os

from .compiler import PyCompiler


def compile_file(file_i: str, file_o: str, key: str) -> None:
    """
    args:
        file_i: the file should be a '.py' file.
        file_o: use the same extension name ('.py') as `file_i`.
    """
    compiler = PyCompiler(key, os.path.dirname(file_o))
    compiler.compile_file(file_i, file_o)


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
