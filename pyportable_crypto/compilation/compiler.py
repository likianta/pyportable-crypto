import importlib.util
import sys
from types import ModuleType

from lk_utils import fs

from ..cipher_gen import cipher_standalone as core
from ..cipher_gen import generate_cipher_package


class PyCompiler:
    runtime_pkgdir: str
    _decrypt: core.decrypt
    _encrypt: core.encrypt
    
    def __init__(self, key: str, _runtime: ModuleType = None) -> None:
        if _runtime:
            self.runtime_pkgdir = fs.parent(_runtime.__file__)
            self._encrypt = _runtime.encrypt
            self._decrypt = _runtime.decrypt
        else:
            assert key, '`key` is required to generate the runtime package.'
            self.runtime_pkgdir = generate_cipher_package(key)
            sys.path.insert(0, fs.parent(self.runtime_pkgdir))
            import pyportable_runtime  # noqa
            # pyportable_runtime = load_package(self.runtime_pkgdir)
            self._encrypt = pyportable_runtime.encrypt
            self._decrypt = pyportable_runtime.decrypt
        self._template = (
            'globals().update('
            'pyportable_runtime.decrypt({cipher_text}, globals(), locals())'
            ')'
            #   if `pyportable_runtime` raised ModuleNotFoundError, you should -
            #   call `import pyportable_runtime; pyportable_runtime.setup()` -
            #   at the very first place.
        )
    
    @classmethod
    def init_from_runtime(cls, runtime: ModuleType) -> 'PyCompiler':
        return cls('', _runtime=runtime)
    
    # -------------------------------------------------------------------------
    
    def compile_file(self, file_i: str, file_o: str) -> None:
        if fs.filename(file_i) == '__init__.py':
            print(':rp', '[green]{}[/]'.format(file_o))
            fs.copy_file(file_i, file_o, True)
        else:
            print(':rp', '[magenta]{}[/]'.format(file_o))
            text = self._encrypt(fs.load(file_i), add_shell=True)
            code = self._template.format(cipher_text=text)
            fs.dump(code, file_o)
    
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
        fs.clone_tree(dir_i, dir_o, True)
        # for d in fs.findall_dirs(dir_i):
        #     fs.make_dir(f'{dir_o}/{d.relpath}')
        for f in fs.findall_files(dir_i, filter=True):
            file_i = f.path
            file_o = f'{dir_o}/{f.relpath}'
            if f.ext == 'py':
                if f.name == '__init__.py':
                    print(':rpi', '[green]{}[/]'.format(f.relpath))
                    fs.copy_file(file_i, file_o, True)
                else:
                    print(':rpi', '[magenta]{}[/]'.format(f.relpath))
                    text = self._encrypt(fs.load(file_i), add_shell=True)
                    code = self._template.format(cipher_text=text)
                    fs.dump(code, file_o)
            elif include_other_files:
                print(':rpi', '[bright_black]{}[/]'.format(f.relpath))
                fs.copy_file(file_i, file_o, True)
        print(':i0s')


def load_package(pkg_dir: str, name: str = None) -> ModuleType:
    """
    ref: https://stackoverflow.com/a/50395128
    """
    init_file = f'{pkg_dir}/__init__.py'
    assert fs.exist(init_file)
    if not name: name = fs.basename(pkg_dir)
    spec = importlib.util.spec_from_file_location(name, init_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # sys.modules[name] = module
    return module
