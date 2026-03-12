import os
from hashids import Hashids

salt = os.getenv("HASHIDS_SALT")

if not salt:
    raise ValueError("HASHIDS_SALT is not defined in environment variables")

hashids = Hashids(
    salt=salt,
    alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    min_length=5,
)

def encode_id(number: int) -> str:
    return hashids.encode(number)


def decode_code(code: str) -> int | None:
    decoded = hashids.decode(code)

    if decoded:
        return decoded[0]

    return None