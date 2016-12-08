import pytest
from block_chain_bucks import BlockChain, Block
from Crypto.Hash.SHA256 import SHA256Hash as SHA256


def test_blockchain_monolithic():
    genesis_payload = b"Genesis"
    genesis_hash_pointer = SHA256(genesis_payload).digest()
    genesis_block = Block(genesis_hash_pointer, genesis_payload)
    payload_1 = b"My payload"
    payload_2 = b"Another one of mine"
    payload_3 = b"My last payload"

    block_chain = BlockChain(genesis_block)
    assert len(block_chain) == 1
    assert block_chain.latest_block.payload == genesis_payload
    block_chain.verify()

    block_chain.append(payload_1)
    assert len(block_chain) == 2
    assert block_chain.latest_block.payload == payload_1
    block_chain.verify()

    block_chain.append(payload_2)
    assert len(block_chain) == 3
    assert block_chain.latest_block.payload == payload_2
    block_chain.verify()

    block_chain.append(payload_3)
    assert len(block_chain) == 4
    assert block_chain.latest_block.payload == payload_3
    block_chain.verify()

    # Replace block in chain
    bad_block_payload = b"I am a malicious payload"
    bad_block_hash_pointer = block_chain.blocks[2].hash_pointer
    bad_block = Block(bad_block_hash_pointer, bad_block_payload)
    block_chain.blocks[2] = bad_block
    with pytest.raises(RuntimeError):
        block_chain.verify()
