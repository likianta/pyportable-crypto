import importlib.util
from os.path import basename
from os.path import exists
from textwrap import dedent
from types import ModuleType

from lk_utils import dumps
from lk_utils import fs
from lk_utils import loads

from ..cipher_gen import cipher_standalone as core
from ..cipher_gen import generate_cipher_package


class PyCompiler:
    _decrypt: core.decrypt
    _encrypt: core.encrypt
    _root: str
    
    def __init__(self, key: str, dir_o: str, **kwargs) -> None:
        self._root = fs.abspath(dir_o)
        self._generate_cipher_runtime(
            runtime_dir := '{}/pyportable_runtime'.format(self._root),
            key,
            _reuse=kwargs.get('reuse_runtime', False),
            _overwrite=kwargs.get('overwrite_runtime', False),
        )
        
        pyportable_runtime = load_package(runtime_dir)
        self._encrypt = pyportable_runtime.encrypt
        self._decrypt = pyportable_runtime.decrypt
        
        self._template = dedent('''
            try:
                from pyportable_runtime import decrypt
            except ImportError:
                import os
                import sys
                search_path = os.path.abspath(f'{{__file__}}/../{relpath}')
                sys.path.insert(0, search_path)
                from pyportable_runtime import decrypt
            finally:
                globals().update(decrypt({cipher_text}))
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
        generate_cipher_package(dir_o, key)
    
    def compile_file(self, file_i: str, file_o: str) -> None:
        if fs.filename(file_i) == '__init__.py':
            print(':rp', '[green]{}[/]'.format(file_o))
            fs.copy_file(file_i, file_o, True)
        else:
            print(':rp', '[magenta]{}[/]'.format(file_o))
            encrypted_text = self._encrypt(loads(file_i), add_shell=True)
            relpath = fs.relpath(self._root, fs.parent(file_i))
            if relpath == '.': relpath = ''
            code = self._template.format(
                cipher_text=encrypted_text,
                relpath=relpath,
            )
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
                    encrypted_text = self._encrypt(loads(file_i), add_shell=True)
                    relpath = fs.relpath(self._root, f.dir)
                    if relpath == '.': relpath = ''
                    code = self._template.format(
                        cipher_text=encrypted_text,
                        relpath=relpath,
                    )
                    dumps(code, file_o)
            elif include_other_files:
                print(':rpi', '[bright_black]{}[/]'.format(f.relpath))
                fs.copy_file(file_i, file_o, True)
        print(':i0s')


def load_package(pkg_dir: str, name: str = None) -> ModuleType:
    """
    ref: https://stackoverflow.com/a/50395128
    """
    init_file = f'{pkg_dir}/__init__.py'
    assert exists(init_file)
    if not name: name = basename(pkg_dir)
    spec = importlib.util.spec_from_file_location(name, init_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # sys.modules[name] = module
    return module
