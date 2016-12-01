from pychat.crypto.work import hash as work
from hashlib import sha256


prefix = b"0123456789abcdef"


def _trailing_zero_count(some_bytes):
    # Dumb trailing zero bit counting
    bit_str = bin(int(some_bytes.hex(), 16))
    return len(bit_str) - len(bit_str.rstrip('0'))


def test_hash_bits_only_1():
    number = 3
    suffix = work(prefix, number)
    result = sha256(prefix + suffix).digest()
    assert _trailing_zero_count(result) >= number

def test_hash_bits_only_2():
    number = 7
    suffix = work(prefix, number)
    result = sha256(prefix + suffix).digest()
    assert _trailing_zero_count(result) >= number

def test_hash_bytes_only_1():
    number = 8
    suffix = work(prefix, number)
    result = sha256(prefix + suffix).digest()
    assert _trailing_zero_count(result) >= number

def test_hash_bytes_only_2():
    number = 16
    suffix = work(prefix, number)
    result = sha256(prefix + suffix).digest()
    assert _trailing_zero_count(result) >= number

def test_hash_bits_and_bytes_1():
    number = 13
    suffix = work(prefix, number)
    result = sha256(prefix + suffix).digest()
    assert _trailing_zero_count(result) >= number

def test_hash_bits_and_bytes_2():
    number = 19
    suffix = work(prefix, number)
    result = sha256(prefix + suffix).digest()
    assert _trailing_zero_count(result) >= number
