import os
import shutil
from textwrap import dedent, indent

import dill
from lk_utils import dumps
from lk_utils import loads

curr_dir = os.path.dirname(__file__)
template = f'{curr_dir}/template'


def generate_custom_cipher_package(key: str, dir_o: str):
    assert key, '`key` must not be empty!'
    assert not os.path.exists(dir_o) or not os.listdir(dir_o), \
        f'`dir_o` ({dir_o}) must be unexisted or empty!'
    
    if not os.path.exists(dir_o): os.mkdir(dir_o)
    if not os.path.isabs(dir_o): dir_o = os.path.abspath(dir_o)
    
    dir_i = template
    
    shutil.copyfile(f'{dir_i}/__init__.txt', f'{dir_o}/__init__.py')
    shutil.copyfile(f'{dir_i}/dill_loader.py', f'{dir_o}/dill_loader.py')
    
    cipher_code = loads(f'{curr_dir}/cipher_standalone.py')
    # assert there is only one placeholder named '__KEY__'
    cipher_code = cipher_code.replace('__KEY__', key)
    cipher_code = loads(f'{dir_i}/cipher.txt').format(
        SOURCE_CODE=indent(cipher_code, '    ').lstrip(),
        DILL_PARENT_DIR=os.path.dirname(os.path.dirname(dill.__file__)),
        # TARGET_DIR=dir_o,
    )
    dumps(cipher_code, f'{dir_o}/cipher.py')
    
    # generate 'cipher.pkl' from 'cipher.py'
    exec(dedent('''
        import os
        import sys
        os.chdir(dir_o)
        sys.path.insert(0, dir_o)
        
        import cipher
        # cipher.main()
    '''), {'dir_o': dir_o, 'dill': dill})
    
    # os.remove(f'{dir_o}/cipher.py')
    return dir_o


if __name__ == '__main__':
    print(generate_custom_cipher_package('hello world', './temp/cipher_test_10'))
