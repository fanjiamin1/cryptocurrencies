from hashlib import sha256
from os import urandom


ZERO_BYTE = b'\x00'

BIT_SIZE = 1
SHAVE_AND_A_HAIRCUT = 2*BIT_SIZE  # 2
NIBBLE = 2*SHAVE_AND_A_HAIRCUT  # 4
BYTE_SIZE = 2*NIBBLE  # 8
CHOMP_SIZE = 2*BYTE_SIZE  # 16
DINNER_SIZE = 2*CHOMP_SIZE  # 32


def hash(prefix, bits):
    assert len(prefix) == CHOMP_SIZE
    assert 0 <= bits <= DINNER_SIZE
    # Create hash object for the prefix
    prefix_hash = sha256(prefix)
    if bits > BYTE_SIZE:
        # Need to check bytes
        check_bytes = bits//BYTE_SIZE
        check_bits = bits % BYTE_SIZE
        expected_end = ZERO_BYTE*check_bytes
        if check_bits == 0:
            # Only need to check bytes
            while True:
                total_hash = prefix_hash.copy()
                suffix = urandom(CHOMP_SIZE)
                total_hash.update(suffix)
                digest = total_hash.digest()
                if digest.endswith(expected_end):
                    return suffix
        else:
            # Need to check bits and bytes
            check_mod = 1 << check_bits
            byte_index = -1 - check_bytes
            while True:
                total_hash = prefix_hash.copy()
                suffix = urandom(CHOMP_SIZE)
                total_hash.update(suffix)
                digest = total_hash.digest()
                if digest.endswith(expected_end):
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
