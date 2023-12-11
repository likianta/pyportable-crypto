"""
requirements:
    python packages:
        cython
        lk-logger
        lk-utils
    if you are using windows:
        download mingw-w64 (https://sourceforge.net/projects/mingw-w64/files/)
        and add it to environment PATH. then tested in cmd: `gcc --version`
    if you are using linux or macos:
        make sure you have gcc installed.
"""
import re
import sys
from platform import system
from random import randint
from textwrap import dedent

from lk_utils import dumps
from lk_utils import fs
from lk_utils import loads
from lk_utils import run_cmd_args
from lk_utils import xpath

system = system().lower()


def generate_cipher_package(
    dir_o: str, key: str, python_executable_path: str = sys.executable
) -> str:
    """
    params:
        key: the secret key.
            - can be any string with any length.
            - cannot be empty.
        dir_o:
            the dirname must be a valid python package name, for example \
            "pyportable_runtime".
            for safety consideration, if the dir_o exists, will stop and raise \
            FileExistsError.
    """
    assert not fs.exists(dir_o), dir_o
    assert key, 'key cannot be empty!'
    assert re.compile(r'[a-zA-Z_]\w*'), \
        'the dirname should be a valid python package name format!'
    
    package_name = fs.dirname(dir_o)
    print(':v2', package_name, key)
    
    dir_i = xpath('.')  # current dir
    # dir_m = kwargs.get('temp_dir', xpath(f'cache/{token_hex()}'))
    dir_m = xpath('cache/{}'.format(
        ''.join(map(str, (randint(0, 9) for _ in range(8))))
    ))
    fs.make_dir(dir_m)
    fs.make_dir(dir_o)
    
    file_i = dir_i + '/cipher_standalone.py'
    file_m = dir_m + '/cipher.py'
    file_o = dir_o + ('/cipher.pyd' if system == 'windows' else '/cipher.so')
    
    code = loads(file_i)
    assert '__KEY__' in code
    code = code.replace('__KEY__', key)
    dumps(code, file_m)
    
    print('compiling... (this may take several minutes)', ':v3st2')
    run_cmd_args(
        python_executable_path,
        # note we don't use abspath because the path in poetry virtual env \
        # may be very long, which will cause windows msvc linking crashed.
        'cythonize.py',  # file in current dir.
        fs.relpath(file_m, dir_i),
        'build_ext',
        '--inplace',
        cwd=dir_i,
    )
    print('compilation done', ':t2')
    
    file_m = fs.find_file_paths(dir_m, ('.pyd', '.so'))[0]
    fs.move(file_m, file_o)
    
    # make it to be package (create '__init__.py')
    from pyportable_crypto import __version__ as crypto_version
    pyversion = sys.version_info[:2]  # e.g. (3, 8)
    dumps(dedent('''\
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
    ''').strip().format(pyversion, crypto_version), dir_o + '/__init__.py')
    
    # clean up intermediate folder
    fs.remove_tree(dir_m)
    
    print('done. see result at "{}"'.format(dir_o), ':t')
    return package_name


if __name__ == '__main__':
    from secrets import token_urlsafe
    generate_cipher_package('../../tests/folder0', token_urlsafe())
