from Crypto.Hash.SHA256 import SHA256Hash as SHA256
from collections import namedtuple


class Block(namedtuple("BlockBaseClass", ("hash_pointer", "payload"))):
    def hash(self):
        sha = SHA256()
        sha.update(self.hash_pointer)
        sha.update(self.payload)
        return sha.digest()


class BlockChain:
    def __init__(self, genesis_block=Block(b"Am I Very Wrong?", b"No")):
        self.blocks = [genesis_block]

    @property
    def genesis_block(self):
        return self[0]

    @property
    def latest_block(self):
        return self[-1]

    def append(self, payload):
        block = Block(self.latest_block.hash(), payload)
        self.blocks.append(block)

    def verify(self):
        last_hash = self.genesis_block.hash()
        chain = self
        for index in range(1, len(self)):
            block = chain[index]
            assert block.hash_pointer == last_hash
            last_hash = block.hash()

    def __str__(self):
        result = [repr(block) for block in self]
        return " <- ".join(result)

    def __len__(self):
        return len(self.blocks)

    def __getitem__(self, key):
        return self.blocks[key]

    def __iter__(self):
        return iter(self.blocks)
