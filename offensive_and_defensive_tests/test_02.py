"""
https://stackoverflow.com/questions/11625923/can-we-access-inner-function
-outside-its-scope-of-outer-function-in-python-using
"""
from lk_logger import lk

from pyportable_crypto import inject

# lk.enable_lite_mode()
# lk.logp = print
# lk.loga = print

# show hidden members
lk.logp(inject.__code__)
lk.logp(inject.__code__.co_consts)

# exec `__example_keygen`
lk.loga(
    inject.__code__.co_consts[2],
    exec(inject.__code__.co_consts[2])
)

# modify inner func
# inject.__code__.co_consts[2] = lambda *args, **kwargs: None
# -> TypeError: 'tuple' object does not support item assignment

# convert to list
# inject.__code__.co_consts = list(inject.__code__.co_consts)
# -> AttributeError: readonly attribute

# AESCBC = inject.__code__.co_consts[18]
lk.loga(exec(inject.__code__.co_consts[18]))
AESCBC = exec(inject.__code__.co_consts[18] + '\n__X__.update(globals())', x := {
    '__X__': {}
})
lk.loga(x)
lk.loga(AESCBC)

cipher = AESCBC(b'xxxxyyyyxxxxyyyy')
a = cipher.encrypt(b'aaaabbbbaaaabbbb')
lk.loga(a)
b = cipher.decrypt(a)
lk.loga(b)
