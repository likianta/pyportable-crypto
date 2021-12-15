import os
from sys import argv
from sys import path

curr_dir = os.path.dirname(__file__)
os.chdir(curr_dir)
path.append(curr_dir + '/site-packages.zip')

from setuptools import setup  # noqa
from Cython.Build import cythonize  # noqa

# usage: <python> <this_file> <file_to_be_compiled>
# e.g. python ./template.py ./hello_world.py
filepath = argv.pop(1)
file_dir, filename = os.path.split(filepath)
os.chdir(file_dir)
setup(ext_modules=cythonize(filename, language_level='3'))
