import base64
import binascii
import typing as t
from collections import namedtuple


Codec = namedtuple('Codec', ['encode', 'decode'])


class T:
    FormatterName = t.Literal['raw', 'binascii', 'base64']
    Formatters = t.Dict[str, Codec]


formatters = {
    'raw': Codec(lambda x: x, lambda x: x),
    'binascii': Codec(binascii.hexlify, binascii.unhexlify),
    'base64': Codec(base64.b64encode, base64.b64decode),
    # TODO: emoji formatter
}
