from lk_logger import lk

import pyportable_crypto
from pyportable_crypto import encrypt_data
from pyportable_crypto.inject import inject

key = '{KEY}'

lk.loga(pyportable_crypto)
lk.loga(pyportable_crypto.inject)


# noinspection PyUnusedLocal
def do_nothing(*args, **kwargs):
    pass


g = inject.__globals__
# lk.logp(g)
# l = inject.__locals__
# lk.logp(l)
# g['_validate_source_file'] = do_nothing
# g['_validate_self_package'] = do_nothing


inject(__file__, globals(), locals(),
       encrypt_data('print("hijack")\n__PYMOD_HOOK__.update(globals())', key))

# _validate_source_file = do_nothing
# _validate_self_package = do_nothing

# inject('')
