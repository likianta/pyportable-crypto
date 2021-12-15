"""
requirements:
    python packages:
        cython
        lk-logger
        lk-utils
    if you are using windows:
        download mingw-w64 and add it to environment PATH.
        tested in cmd: `gcc --version`
    if you are using linux or macos:
        make sure you have gcc installed.
"""
import os.path
import shutil
import sys
from secrets import token_hex
from time import time

from lk_logger import lk
from lk_utils import dumps
from lk_utils import loads
from lk_utils import run_cmd_args
from lk_utils.filesniff import currdir


def main(key, dist_dir, python_executable_path=sys.executable):
    """
    Args:
        key: str
        dist_dir: str.
            we will generate a "pyportable_runtime" package in this directory.
            if `dist_dir` doesn't exist, we will create it.
            if `pyportable_runtime` already exists, it raises an exception.
            it is suggested to use a directory name ends with python version
            info. for example 'my_custom_runtime_py3.7'.
        python_executable_path: str.
            the path to regular python interpreter which is installed in your
            computer.
            the site-packages are relateless. we will use our own in this
            folder.
    """
    assert key, 'key cannot be empty'
    if not os.path.exists(dist_dir):
        os.mkdir(dist_dir)
    else:
        assert not os.path.exists(dist_dir + '/pyportable_runtime'), (
            f'make sure no "pyportable_runtime" package exists in "{dist_dir}"'
        )
    
    dir_i = '../pyportable_crypto/cipher_gen'
    dir_m = currdir() + '/cache/' + token_hex()  # intermediate folder
    dir_o = dist_dir + '/pyportable_runtime'
    os.mkdir(dir_m)
    os.mkdir(dir_o)
    
    file_i = dir_i + '/cipher_standalone.py'
    file_m = dir_m + '/cipher.py'
    file_o = dir_o + '/cipher.pyd'
    
    code = loads(file_i)
    code = code.replace('__key__', key)
    dumps(code, file_m)
    
    lk.loga('compiling... (this may take several minutes)')
    start = time()
    run_cmd_args(
        python_executable_path,
        currdir() + '/cythonize.py',
        os.path.abspath(file_m), 'build_ext', '--inplace'
    )
    lk.loga('compilation consumed {:.2f}s'.format(time() - start))
    
    file_m = dir_m + '/' + \
             [x for x in os.listdir(dir_m) if x.endswith(('.pyd', '.so'))][0]
    shutil.move(file_m, file_o)
    
    # make it to be package
    from textwrap import dedent
    from pyportable_crypto import __version__ as crypto_version
    pyversion = run_cmd_args(python_executable_path, '--version')
    pyversion = tuple(map(int, pyversion.split(' ')[1].split('.')[:2]))
    #   e.g. 'Python 3.8.10' -> (3, 8)
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
    try:
        shutil.rmtree(dir_m)
    except:  # usually failed due to permission error...
        pass

    lk.loga('see result: {}'.format(dir_o))
    return dir_o


if __name__ == '__main__':
    main('abc123', '../tests/folder1')
