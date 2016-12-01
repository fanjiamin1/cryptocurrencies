from hashlib import sha256
from os import urandom


ZERO_BYTE = '\x00'

BIT_SIZE = 1
SHAVE_AND_A_HAIRCUT = 2*BIT_SIZE
NIBBLE = 2*SHAVE_AND_A_HAIRCUT
BYTE_SIZE = 2*NIBBLE
CHOMP_SIZE = 2*BYTE_SIZE


def hash(prefix, bits):
    assert len(prefix) == CHOMP_SIZE
    # Create hash object for the prefix
    prefix_hash = sha256(prefix)
    if bits > BYTE_SIZE:
        # Need to check bytes
        check_bytes = bits//BYTE_SIZE
        check_bits = bits % BYTE_SIZE
        slice_index = -check_bytes
        if check_bits == 0:
            # Only need to check bytes
            while True:
                total_hash = prefix_hash.copy()
                suffix = urandom(CHOMP_SIZE)
                total_hash.update(suffix)
                digest = total_hash.digest()
                if all(byte == 0 for byte in digest[slice_index:]):
                    return suffix
        else:
            # Need to check bits and bytes
            check_mod = 1 << check_bits
            byte_index = slice_index - 1
            while True:
                total_hash = prefix_hash.copy()
                suffix = urandom(CHOMP_SIZE)
                total_hash.update(suffix)
                digest = total_hash.digest()
                if all(byte == 0 for byte in digest[slice_index:]):
                    print(digest[byte_index])
                    if digest[byte_index] % check_mod == 0:
                        return suffix
    else:
        # No need to check bytes
        check_mod = 1 << bits
        while True:
            total_hash = prefix_hash.copy()
            suffix = urandom(CHOMP_SIZE)
            total_hash.update(suffix)
            digest = total_hash.digest()
            if digest[-1] % check_mod == 0:
                return suffix
