import base64
import binascii
from collections import namedtuple

_codec = namedtuple('FormatterCodec', ['encode', 'decode'])

formatters = {
    'raw'     : _codec(lambda x: x, lambda x: x),
    'binascii': _codec(binascii.hexlify, binascii.unhexlify),
    'base64'  : _codec(base64.b64encode, base64.b64decode),
    # TODO: emoji formatter
}
