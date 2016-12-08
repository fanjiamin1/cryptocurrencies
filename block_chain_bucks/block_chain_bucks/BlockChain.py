from Crypto.Hash.SHA256 import SHA256Hash as SHA256
from collections import namedtuple


class Block(namedtuple("BlockBaseClass", ("hash_pointer", "payload"))):
    ENCODING = "utf-8"
    PAYLOAD_SIZE = 2**10  # 1 Kilobyte
    HASH_POINTER_SIZE = 32  # Bytes

    def __init__(self, hash_pointer, payload):
        if not isinstance(hash_pointer, (bytes, bytearray)):
            message = "{} object is not bytes/bytearray".format(repr(hash_pointer))
            raise TypeError(message)
        if len(hash_pointer) != Block.HASH_POINTER_SIZE:
            message = "Non-{} byte hash length".format(Block.HASH_POINTER_SIZE)
            raise ValueError(message)
        if not isinstance(payload, (bytes, bytearray)):
            payload = bytearray(payload, ENCODING)
        if len(payload) > Block.PAYLOAD_SIZE:
            message = "Payload exceeds maximum payload size"
            raise ValueError(message)

    def hash(self):
        sha = SHA256()
        sha.update(self.hash_pointer)
        sha.update(self.payload)
        return sha.digest()


class BlockChain:
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
            assert block.hash_pointer == last_hash
            last_hash = block.hash()

    def find_balance(self,id):
        for block in reversed(self):
            transaction_words=block.payload.split(' ')
            out_id_index=-1
            if id in transaction:
                #pythonic way of finding output part of the id
                out_id_index=transaction_words[:transaction_words.index(id)+1].index(id)+transaction_words.index(id)+1
                out_amount_index = out_id_index+1
                break
            if out_id_index==-1:
                #TODO:need to account for founder transaction
                #otherwise no balance can ever exist
                return 0
        try:
            return int(transaction_words[out_amount_index])
        except:
            #this means we have a malformed transaction in the block-chain
            system.exit("blockchain contained invalid transfer or balance checking is bugged")

    def __str__(self):
        result = [repr(block) for block in self]
        return " <- ".join(result)

    def __len__(self):
        return len(self.blocks)

    def __getitem__(self, key):
        return self.blocks[key]

    def __iter__(self):
        return iter(self.blocks)
