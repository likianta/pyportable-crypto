from lk_utils import dumps
from lk_utils import fs
from lk_utils import loads

from .cipher_gen import cipher_standalone as core


class PyCompiler:
    _decrypt: core.decrypt
    _encrypt: core.encrypt
    
    def __init__(self, key: str, dir_o: str, **kwargs):
        self._generate_cipher_runtime(
            runtime_dir := '{}/pyportable_runtime'.format(fs.parent(dir_o)),
            key,
            _reuse=kwargs.get('reuse_runtime', False),
            _overwrite=kwargs.get('overwrite_runtime', False),
        )
        
        import sys
        sys.path.insert(0, fs.parent(runtime_dir))
        
        from pyportable_runtime import encrypt, decrypt  # noqa
        self._encrypt = encrypt
        self._decrypt = decrypt
        
        from textwrap import dedent
        self._template = dedent('''
            from pyportable_runtime import decrypt
            globals().update(decrypt({ciphertext}, globals(), locals()))
        ''').strip()
    
    @staticmethod
    def _generate_cipher_runtime(
        dir_o: str,
        key: str,
        _reuse: bool = False,
        _overwrite: bool = False
    ) -> None:
        if fs.exists(dir_o):
            if _reuse:
                return
            elif _overwrite:
                fs.remove_tree(dir_o)
            else:
                raise FileExistsError(dir_o)
        from .cipher_gen import generate_cipher_package
        generate_cipher_package(dir_o, key)
    
    def compile_file(self, file_i: str, file_o: str) -> None:
        if fs.filename(file_i) == '__init__.py':
            print(':rp', '[green]{}[/]'.format(file_o))
            fs.copy_file(file_i, file_o, True)
        else:
            print(':rp', '[magenta]{}[/]'.format(file_o))
            data = self._encrypt(loads(file_i), add_shell=True)
            code = self._template.format(ciphertext=data)
            dumps(code, file_o)
    
    def compile_dir(
        self, dir_i: str, dir_o: str, include_other_files: bool = True
    ) -> None:
        """
        output structure:
            <the_parent_of_dir_o>
            |= pyportable_runtime
                |- __init__.py
                |- cipher.so  # or "cipher.pyd"
            |= <dir_o>
                |- __init__.py
                |- ...
        """
        fs.clone_tree(dir_i, dir_o)
        # for d in fs.findall_dirs(dir_i):
        #     fs.make_dir(f'{dir_o}/{d.relpath}')
        for f in fs.findall_files(dir_i):
            file_i = f.path
            file_o = f'{dir_o}/{f.relpath}'
            if f.ext == 'py':
                if f.name == '__init__.py':
                    print(':rpi', '[green]{}[/]'.format(f.relpath))
                    fs.copy_file(file_i, file_o, True)
                else:
                    print(':rpi', '[magenta]{}[/]'.format(f.relpath))
                    data = self._encrypt(loads(file_i), add_shell=True)
                    code = self._template.format(ciphertext=data)
                    dumps(code, file_o)
            elif include_other_files:
                print(':rpi', '[bright_black]{}[/]'.format(f.relpath))
                fs.copy_file(file_i, file_o, True)
        print(':i0s')
