import sys
from hashlib import md5
from platform import system

import lk_logger
from lk_utils import dedent
from lk_utils import dump
from lk_utils import fs
from lk_utils import run_cmd_args

SYSTEM = system().lower()


def generate_cipher_package(
    key: str, python_executable_path: str = sys.executable
) -> str:
    """
    params:
        key: the secret key.
            - can be any string with any length.
            - cannot be empty.
    """
    from .. import __version__ as crypto_version
    
    assert key, 'key cannot be empty!'
    # assert re.compile(r'[a-zA-Z_]\w*'), \
    #     'the dirname should be a valid python package name format!'
    
    dir_i = fs.xpath('.')  # current dir
    dir_m = fs.xpath('_cache/{}'.format(
        md5('{}@{}'.format(key, crypto_version).encode('utf-8')).hexdigest()
    ))
    dir_o = '{}/pyportable_runtime'.format(dir_m)
    if fs.exist(dir_o):
        return dir_o
    else:
        fs.make_dirs(dir_o)
    
    file_i = '{}/cipher_standalone.py'.format(dir_i)
    file_m = '{}/cipher.py'.format(dir_m)
    file_o = '{}/cipher.{}'.format(
        dir_o, 'pyd' if SYSTEM == 'windows' else 'so'
    )
    
    # -------------------------------------------------------------------------
    
    code = fs.load(file_i)
    assert '__KEY__' in code
    code = code.replace('__KEY__', key)
    fs.dump(code, file_m)
    
    with lk_logger.spinner('compiling... (this may take several minutes)'):
        with lk_logger.timing(True):
            try:
                run_cmd_args(
                    python_executable_path,
                    # note we don't use abspath because the path in poetry -
                    # virtual env may be very long, which will cause windows -
                    # msvc linking crashed.
                    'cythonize.py',  # file in current dir.
                    fs.relpath(file_m, dir_i),
                    'build_ext',
                    '--inplace',
                    cwd=dir_i,
                )
            except Exception:
                fs.remove_tree(dir_o)
                raise
    fs.move(fs.find_file_paths(dir_m, ('.pyd', '.so'))[0], file_o)
    
    pyversion = sys.version_info[:2]  # e.g. (3, 8)
    dump(
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
                    "Python interpreter version is not matched! "
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
        f'{dir_o}/__init__.py'
    )
    
    return dir_o
