import os
from hashids import Hashids

hashids = Hashids(
    salt=os.getenv("HASHIDS_SALT"),
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