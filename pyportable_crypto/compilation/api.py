from lk_utils import fs

from .compiler import PyCompiler


def compile_file(
    file_i: str, file_o: str, key: str, add_runtime_package: bool = True
) -> None:
    """
    args:
        file_i: the file should be a '.py' file.
        file_o: use the same extension name ('.py') as `file_i`.
    """
    compiler = PyCompiler(key)
    compiler.compile_file(file_i, file_o)
    if add_runtime_package:
        fs.copy_tree(
            compiler.runtime_pkgdir,
            f'{fs.parent(file_o)}/pyportable_runtime'
        )


def compile_dir(
    dir_i: str, dir_o: str, key: str, add_runtime_package: bool = True
) -> None:
    """
    iterate all ".py" files in `dir_i` and compile them to `dir_o`.
    """
    compiler = PyCompiler(key)
    compiler.compile_dir(dir_i, dir_o)
    if add_runtime_package:
        fs.copy_tree(
            compiler.runtime_pkgdir,
            f'{dir_o}/pyportable_runtime'
        )
