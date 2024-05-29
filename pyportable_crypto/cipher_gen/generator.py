import sys
from hashlib import md5
from platform import system

from lk_utils import dumps
from lk_utils import fs
from lk_utils import run_cmd_args
from lk_utils import xpath
from lk_utils.textwrap import dedent

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
    
    dir_i = xpath('.')  # current dir
    dir_m = xpath('_cache/{}'.format(
        md5('{}@{}'.format(key, crypto_version).encode('utf-8')).hexdigest()
    ))
    dir_o = '{}/pyportable_runtime'.format(dir_m)
    if fs.exists(dir_o):
        return dir_o
    else:
        fs.make_dirs(dir_o)
    
    file_i = '{}/cipher_standalone.py'.format(dir_i)
    file_m = '{}/cipher.py'.format(dir_m)
    file_o = '{}/cipher.{}'.format(dir_o, 'pyd' if SYSTEM == 'windows' else 'so')
    
    # -------------------------------------------------------------------------
    
    code = fs.load(file_i)
    assert '__KEY__' in code
    code = code.replace('__KEY__', key)
    fs.dump(code, file_m)
    
    print('compiling... (this may take several minutes)', ':v3st2')
    run_cmd_args(
        python_executable_path,
        # note we don't use abspath because the path in poetry virtual env -
        # may be very long, which will cause windows msvc linking crashed.
        'cythonize.py',  # file in current dir.
        fs.relpath(file_m, dir_i),
        'build_ext',
        '--inplace',
        cwd=dir_i,
    )
    print('compilation done', ':t2')
    fs.move(fs.find_file_paths(dir_m, ('.pyd', '.so'))[0], file_o)
    
    pyversion = sys.version_info[:2]  # e.g. (3, 8)
    dumps(dedent('''
        encrypt = None
        decrypt = None


        def _init_check():
            import sys

            current_pyversion = sys.version_info[:2]  # type: tuple
            target_pyversion = {0}
            if current_pyversion != target_pyversion:
                raise Exception(
                    "Python interpreter version doesn't matched!",
                    "Required: Python {{}}, got {{}} ({{}})".format(
                        ', '.join(map(str, target_pyversion)),
                        ', '.join(map(str, current_pyversion)),
                        sys.executable
                    )
                )


        _init_check()
        del _init_check

        from .cipher import decrypt  # noqa
        from .cipher import encrypt  # noqa

        __version__ = '{1}'
    ''').format(pyversion, crypto_version), f'{dir_o}/__init__.py')
    
    return dir_o
