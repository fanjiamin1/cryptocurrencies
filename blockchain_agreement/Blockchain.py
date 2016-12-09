from builtins import tuple as _tuple
from Crypto.Hash.SHA256 import SHA256Hash as SHA256
from collections import namedtuple


class Block(namedtuple("BlockBaseClass", ("hash_pointer", "payload"))):
    ENCODING = "utf-8"
    PAYLOAD_SIZE = 2**10  # 1 Kilobyte
    HASH_POINTER_SIZE = 32  # Bytes

    def __new__(_cls, hash_pointer, payload):
        if not isinstance(hash_pointer, (bytes, bytearray)):
            message = "'{}' object is not bytes/bytearray"
            message = message.format(type(hash_pointer).__name__)
            raise TypeError(message)
        if len(hash_pointer) != Block.HASH_POINTER_SIZE:
            message = "Non-{} byte hash length"
            message = message.format(Block.HASH_POINTER_SIZE)
            raise ValueError(message)
        if not isinstance(payload, (bytes, bytearray)):
            if isinstance(payload, str):
                payload = bytearray(payload, Block.ENCODING)
            else:
                message = "'{}' object is neither bytes/bytearray nor string"
                message = message.format(type(payload).__name__)
                raise TypeError(message)
        if len(payload) != Block.PAYLOAD_SIZE:
            message = "Incorrect payload size"
            raise ValueError(message)
        return _tuple.__new__(_cls, (hash_pointer, payload))

    def hash(self):
        sha = SHA256()
        sha.update(self.hash_pointer)
        sha.update(self.payload)
        return sha.digest()


class Blockchain:
    def __init__(self, genesis_block=None):
        if genesis_block is None:
            payload = b"Am I Very Wrong?"
            hash_pointer = SHA256(payload).digest()
            genesis_block = Block(hash_pointer, payload)
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
            if block.hash_pointer != last_hash:
                message = "Block chain integrity compromise at index "
                raise RuntimeError(message + str(index))
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
