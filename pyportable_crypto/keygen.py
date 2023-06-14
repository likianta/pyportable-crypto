import secrets


def generate_random_key(bytelen: int = 32) -> str:
    assert bytelen % 2 == 0
    return secrets.token_hex(int(bytelen / 2))


def generate_random_bytes(n: int = 32) -> bytes:
    return secrets.SystemRandom().randbytes(n)
