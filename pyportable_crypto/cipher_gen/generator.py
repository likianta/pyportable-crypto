import sys
import typing as tp
from hashlib import md5
from platform import system

from lk_utils import dedent
from lk_utils import fs
from lk_utils import run_cmd_args
from neoprint import print


def generate_cipher_package(
    key: str,
    dir_o: tp.Optional[str] = None,
    # python_executable_path: str = sys.executable,
    overwrite: bool = False,
) -> str:
    """
    params:
        key: the secret key.
            - can be any string with any length.
            - suggest adding salt with `../encryption/keygen.py:add_salt`.
            - cannot be empty.
    """
    from .. import __version__ as crypto_version

    assert key, 'key cannot be empty!'
    # assert re.compile(r'[a-zA-Z_]\w*'), \
    #     'the dirname should be a valid python package name format!'

    dir0 = fs.here()
    dir1 = fs.there(
        '_cache/{}'.format(
            md5('{}@{}'.format(key, crypto_version).encode('utf-8')).hexdigest()
        )
    )
    dir2 = '{}/pyportable_runtime'.format(dir1)
    dir3 = '{}/pyportable_runtime'.format(dir_o or dir1)
    if fs.exist(dir2):
        if overwrite:
            fs.remove_tree(dir2)
        else:
            if dir2 != dir3:
                fs.make_link(dir2, dir3, True)
            return dir3
    else:
        fs.make_dirs(dir2)

    file0 = '{}/cipher_standalone.py'.format(dir0)
    file1 = '{}/cipher.py'.format(dir1)
    file2 = '{}/cipher.{}'.format(
        dir2, 'pyd' if system().lower() == 'windows' else 'so'
    )
    # file3 = '{}/cipher.{}'.format(
    #     dir3, 'pyd' if system().lower() == 'windows' else 'so'
    # )

    # --------------------------------------------------------------------------

    code = fs.load(file0)
    assert '__KEY__' in code
    code = code.replace('__KEY__', key)  # TODO
    fs.dump(code, file1)

    print(
        ':v5',
        'compiling {} with secret key (this may take a while)'.format(
            fs.basename(file2)
        ),
    )
    try:
        run_cmd_args(
            (
                sys.executable,
                '-m',
                'nuitka',
                '--module',
                'cipher.py',  # file1
                # optimizations
                # https://chatgpt.com/share/6a4490af-5a60-83ee-8bc9-2503f9263f5e
                '--lto=yes',
            ),
            cwd=dir1,
            verbose=True,
        )
    except Exception:
        fs.remove_tree(dir1)
        raise
    else:
        fs.move(fs.find_file_paths(dir1, ('.pyd', '.so'))[0], file2)

    pyversion = sys.version_info[:2]  # e.g. (3, 8)
    fs.dump(
        dedent(
            '''
            """
            how to use:
                import pyportable_runtime
                pyportable_runtime.setup()
                
                import some_encrypted_package
                some_encrypted_package.some_func()
                ...
            """
            import sys as _sys
            _current_pyversion = _sys.version_info[:2]  # type: tuple
            _target_pyversion = {0}
            if _current_pyversion != _target_pyversion:
                raise Exception(
                    "Python interpreter version does not match! "
                    "Required Python {{}}, got {{}} ({{}})".format(
                        ', '.join(map(str, _target_pyversion)),
                        ', '.join(map(str, _current_pyversion)),
                        _sys.executable
                    )
                )
            
            from .cipher import decrypt  # noqa
            from .cipher import encrypt  # noqa
            
            def setup() -> None:
                import builtins
                setattr(builtins, 'pyportable_runtime', _sys.modules[__name__])
            
            __version__ = '{1}'
            '''
        ).format(pyversion, crypto_version),
        f'{dir2}/__init__.py',
    )

    if dir2 != dir3:
        fs.make_link(dir2, dir3, True)

    return dir3
