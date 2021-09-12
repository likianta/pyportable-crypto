import secrets
from uuid import uuid1


def generate_random_key() -> str:
    return str(uuid1())


def generate_random_bytes(n=16) -> bytes:
    return secrets.SystemRandom().randbytes(n)
