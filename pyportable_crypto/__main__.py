try:
    from fire import Fire
except ImportError:
    input('Please install fire first: `pip install fire`')
    import sys
    
    sys.exit(1)
else:
    import os
    from .compiler import Compiler


class CLI:
    
    @staticmethod
    def compile_file(file_i, file_o, key):
        compiler = Compiler(str(key), os.path.dirname(file_o))
        compiler.compile_file(file_i, file_o)
    
    @staticmethod
    def compile_dir(dir_i, dir_o, key):
        compiler = Compiler(str(key), dir_o)
        compiler.compile_dir(dir_i, dir_o)


if __name__ == '__main__':
    Fire(CLI())
