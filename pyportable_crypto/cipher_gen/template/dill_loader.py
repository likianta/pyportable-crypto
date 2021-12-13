"""
Source: https://github.com/uqfoundation/dill
"""
import __main__ as _main_module
from pickle import Unpickler as StockUnpickler


class Unpickler(StockUnpickler):
    """ Python's Unpickler extended to interpreter sessions and more types. """
    
    _session = False
    
    def __init__(self, file_obj):
        super().__init__(file_obj)
        self._main = _main_module
        self._ignore = False
    
    def find_class(self, module, name):
        if (module, name) == ('__builtin__', '__main__'):
            return self._main.__dict__  # XXX: above set w/save_module_dict
        elif (module, name) == ('__builtin__', 'NoneType'):
            return type(None)  # XXX: special case: NoneType missing
        elif module == 'dill.dill':
            raise ModuleNotFoundError(module)
        return super().find_class(module, name)
    
    def load(self):  # NOTE: if settings change, need to update attributes
        obj = StockUnpickler.load(self)
        if type(obj).__module__ == getattr(_main_module, '__name__', '__main__'):
            if not self._ignore:
                # point obj class to main
                try:
                    obj.__class__ = getattr(self._main, type(obj).__name__)
                except (AttributeError, TypeError):
                    pass  # defined in a file
        return obj
    
    load.__doc__ = StockUnpickler.load.__doc__


def load(filepath):
    with open(filepath, 'rb') as f:
        return Unpickler(f).load()


__all__ = ['load']
