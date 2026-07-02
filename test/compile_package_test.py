import sys

from argsense import cli
from neoprint import print

import pyportable_crypto as pyc


@cli
def compile():
    pkgdir = '.venv/Lib/site-packages/lk_utils'
    key = pyc.keygen.random_key()
    print(key, ':n')
    pyc.compile_package(pkgdir, 'test/lk_utils_enc', key=key)


@cli
def test():
    sys.path.insert(0, 'test')
    sys.path.insert(0, 'test/lk_utils_enc')

    import lk_utils_enc  # ty: ignore

    print(lk_utils_enc.fs.get_current_dir(), ':nv2')


if __name__ == '__main__':
    cli.run()
