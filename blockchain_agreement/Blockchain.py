from builtins import tuple as _tuple
from hashlib import sha256 as Hash
from collections import namedtuple


BlockBaseClass = namedtuple("BlockBaseClass", (
                                                "hash_pointer"  #  32 bytes
                                              , "time_stamp"    #  integer
                                              , "comment"       #  string
                                              , "counter"       #  integer
                                              , "difficulty"    #  integer
                                              , "nonce"         #  16 bytes
                                              ))


class Block(BlockBaseClass):
    """Blocks designed specially for this simulation.

    It has a 32 byte hash pointer.
    The rest is partitioned in the following way:
        Time stamp (milliseconds since epoch)
        A document (can be 0 but preferably not)
        Counter increasing with the size of a blockchain
        Integer indicating difficulty of proof-of-work
        16 byte nonce
    """
    HASH_POINTER_SIZE = 32  # Bytes
    NONCE_SIZE = 16

    def __new__(_cls, hash_pointer, time_stamp, comment, counter, difficulty, nonce=b""):
        if not isinstance(hash_pointer, (bytes, bytearray)):
            message = "'{}' object is not bytes/bytearray"
            message = message.format(type(hash_pointer).__name__)
            raise TypeError(message)
        return _tuple.__new__(_cls, (
                                      hash_pointer
                                    , time_stamp
                                    , comment
                                    , counter
                                    , difficulty
                                    , nonce
                                    ))

    @classmethod
    def genesis_block(cls, difficulty=0):
        hash_pointer = b"\x17"*cls.HASH_POINTER_SIZE
        genesis_time = 1000198000*1000
        document = rot_13_this.encode()
        counter = 0
        difficulty = difficulty
        nonce = b"\x17"*16
        return cls(hash_pointer, genesis_time, document, counter, difficulty, nonce)

    def hash(self):
        hash_object = Hash()
        hash_object.update(self.hash_pointer)
        hash_object.update(str(self.block_time).encode())
        hash_object.update(self.comment.encode())
        hash_object.update(str(self.counter).encode())
        hash_object.update(str(self.difficulty).encode())
        hash_object.update(self.nonce)
        return hash_object.digest()


class Blockchain:
    def __init__(self, genesis_block):
        self.blocks = [genesis_block]

    @property
    def genesis_block(self):
        return self[0]

    @property
    def latest_block(self):
        return self[-1]

    def append(self, block):
        if block.hash_pointer != self.latest_block.hash():
            raise ValueError("Illegal block hash pointer")
        self.blocks.append(block)

    def verify(self):
        last_hash = self.genesis_block.hash_pointer
        for index, block in enumerate(self):
            if block.hash_pointer != last_hash or block.counter_value != index:
                message = "Block chain integrity compromise at index {:d}"
                message.format(index)
                raise RuntimeError(message)
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
