import typing as t


class T:
    InData = t.Union[str, bytes]
    Mode = t.Literal['r', 'rb', 'w', 'wb']
    OutData = t.Union[str, bytes]


def load_file(file: str, mode: T.Mode = 'rb') -> T.OutData:
    with open(
            file, mode,
            encoding=None if mode[-1] == 'b' else 'utf-8'
    ) as f:
        return f.read()


def dump_file(data: T.OutData, file: str, mode: T.Mode = None) -> None:
    if mode is None:
        mode = 'wb' if isinstance(data, bytes) else 'w'
    else:
        if mode == 'wb' and isinstance(data, str):
            data = data.encode('utf-8')
        elif mode == 'w' and isinstance(data, bytes):
            data = data.decode('utf-8')
    with open(
            file, mode,
            encoding=None if mode[-1] == 'b' else 'utf-8'
    ) as f:
        f.write(data)
