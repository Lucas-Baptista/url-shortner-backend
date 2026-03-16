import os
from hashids import Hashids

salt = os.getenv("HASHIDS_SALT")
alphabet = os.getenv("HASHID_ALPHABET")

if not salt or not alphabet:
    raise ValueError("HASHIDS_SALT or HASHID_ALPHABET is not defined in environment variables")

hashids = Hashids(
    salt=salt,
    alphabet=alphabet,
    min_length=5,
)

def encode_id(number: int) -> str:
    return hashids.encode(number)


def decode_code(code: str) -> int | None:
    decoded = hashids.decode(code)

    if decoded:
        return decoded[0]

    return None