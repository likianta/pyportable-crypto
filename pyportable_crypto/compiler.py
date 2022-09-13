import os
from typing import Callable
from typing import Union

from lk_utils import dumps
from lk_utils import loads
from lk_utils.filesniff import find_dirs
from lk_utils.filesniff import find_files

from .cipher_gen import cipher_standalone as core


class PyCompiler:
    _encrypt: core.encrypt
    _decrypt: core.decrypt
    
    def __init__(self, key: str, dir_o: str):
        import sys
        from .cipher_gen import generate_custom_cipher_package
        generate_custom_cipher_package(key, dir_o)
        sys.path.insert(0, dir_o)
        
        from pyportable_runtime import encrypt, decrypt  # noqa
        self._encrypt = encrypt
        self._decrypt = decrypt

        from textwrap import dedent
        self._template = dedent('''
            from pyportable_runtime import decrypt
            globals().update(decrypt({ciphertext}, globals(), locals()))
        ''').strip()
    
    def compile_file(self, file_i: str, file_o: str, _p=1):
        # _p:
        #   1: parent (frame)
        #   2: grand-parent (frame)
        #   3: great-grand-parent (frame)
        print('compiling in "{}": {} -> {}'.format(
            os.path.dirname(file_o),
            os.path.basename(file_i),
            os.path.basename(file_o)
        ), f':p{_p}')
        data = self._encrypt(loads(file_i), add_shell=True)
        code = self._template.format(ciphertext=data)
        dumps(code, file_o)
    
    def compile_dir(self, dir_i: str, dir_o: str, suffix=('.py',),
                    file_exists_scheme: Union[str, Callable] = 'raise_error'):
        
        def loop(dir_i, dir_o):
            for fp, fn in find_files(dir_i, suffix=suffix):
                file_i = fp
                file_o = f'{dir_o}/{fn}'
                
                if os.path.exists(file_o):
                    if file_exists_scheme == 'raise_error':
                        raise FileExistsError(f'{file_o} already exists')
                    elif file_exists_scheme == 'skip':
                        continue
                    elif file_exists_scheme == 'overwrite':
                        self.compile_file(file_i, file_o, _p=3)
                    else:  # assume callable
                        file_exists_scheme(file_o)
                else:
                    self.compile_file(file_i, file_o, _p=3)
                
                for dp, dn in find_dirs(dir_i):
                    sub_dir_i = dp
                    sub_dir_o = f'{dir_o}/{dn}'
                    if not os.path.exists(sub_dir_o):
                        os.mkdir(sub_dir_o)
                    loop(sub_dir_i, sub_dir_o)
        
        loop(dir_i, dir_o)
