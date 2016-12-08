import pytest
from block_chain_bucks import Block


good_hash_pointer = bytes(Block.HASH_POINTER_SIZE)
string_payload = "This is a payload"
bytes_payload = b"This is a bytes payload"


def test_block_wrong_type_argument_1():
    with pytest.raises(TypeError):
        Block("Not a good hash pointer", string_payload)

def test_block_wrong_type_argument_2():
    with pytest.raises(TypeError):
        Block(good_hash_pointer, 123)

def test_block_wrong_value_argument_1():
    with pytest.raises(ValueError):
        Block(bytes(Block.HASH_POINTER_SIZE + 1), bytes_payload)

def test_block_wrong_value_argument_2():
    with pytest.raises(ValueError):
        Block(good_hash_pointer, b"A"*(Block.PAYLOAD_SIZE + 1))

def test_block_payload_encoding():
    block = Block(good_hash_pointer, string_payload)
    assert block.payload.decode(Block.ENCODING) == string_payload
