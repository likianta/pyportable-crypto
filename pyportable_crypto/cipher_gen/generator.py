import os
import shutil
import sys
from textwrap import indent

import dill
from lk_utils import dumps
from lk_utils import loads
from lk_utils import run_cmd_args

curr_dir = os.path.dirname(__file__)
template = f'{curr_dir}/template'


def _generate_fingerprint(key: str) -> str:
    from hashlib import md5
    from random import randint
    
    md5_instance = md5()
    md5_instance.update(((key + key[::-1]) * randint(10, 20)).encode('utf-8'))
    #   `(key + key[::-1])`: reduce the probility of collision (for example,
    #       if we use `key` only, it couldn't be detected that if developer
    #       changed last key by replicated.)
    #   `randint(10, 20)`: repeat with random times to make it harder to guess.
    #       (against the attackers)
    return md5_instance.hexdigest()


def _validate_fingerprint(fingerprint: str, key: str):
    for i in range(10, 21):
        if _generate_fingerprint(key * i) == fingerprint:
            return True
    return False


class ProcessFinished(Exception):
    pass


def _init_check(key, dir_o):
    assert key, '`key` must not be empty!'
    assert os.path.exists(dir_o), f'`dir_o` ({dir_o}) must exist!'
    
    if os.path.exists(f'{dir_o}/pyportable_runtime'):
        sys.path.append(dir_o)
        
        import pyportable_runtime as ppr  # noqa
        from .. import __version__
        if ppr.__version__ == __version__:
            if _validate_fingerprint(ppr.fingerprint, key):
                raise ProcessFinished
        
        raise FileExistsError(
            'pyportable-runtime package already exists in target folder! '
            'please move or delete it to re-generate.'
        )


def generate_custom_cipher_package(key: str, dir_o: str):
    try:
        _init_check(key, dir_o)
    except ProcessFinished:
        return
    except Exception as e:
        raise e
    
    dir_i = template
    dir_o = f'{dir_o}/pyportable_runtime'
    os.mkdir(dir_o)
    
    # file (1/3): __init__.py
    _generate_file_0(f'{dir_i}/__init__.txt', f'{dir_o}/__init__.py', key)
    # file (2/3): dill_loader.py
    _generate_file_1(f'{dir_i}/dill_loader.py', f'{dir_o}/dill_loader.py')
    # file (3/3): cipher.py
    _generate_file_2(f'{dir_i}/cipher.txt', f'{dir_o}/cipher.py', key)
    # generate 'cipher.pkl' from 'cipher.py'
    _generate_file_3(f'{dir_o}/cipher.py')
    
    return dir_o


def _generate_file_0(file_i, file_o, key):
    from .. import __version__
    text = loads(file_i)
    text = text.format(
        VERSION=__version__,
        FINGERPRINT=_generate_fingerprint(key),
    )
    dumps(text, file_o)


def _generate_file_1(file_i, file_o):
    shutil.copyfile(file_i, file_o)


def _generate_file_2(file_i, file_o, key):
    code = loads(f'{curr_dir}/cipher_standalone.py')
    # assert there is only one placeholder named '__KEY__'
    code = code.replace('__KEY__', key)
    code = loads(file_i).format(
        SOURCE_CODE=indent(code, '    ').lstrip(),
        DILL_PARENT_DIR=os.path.dirname(os.path.dirname(dill.__file__)),
    )
    dumps(code, file_o)


def _generate_file_3(file_i):
    run_cmd_args(sys.executable, file_i)
    os.remove(file_i)


if __name__ == '__main__':
    print(generate_custom_cipher_package(
        'hello world', '../../tests/cipher_test_3'
    ))
