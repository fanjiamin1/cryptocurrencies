from Crypto.Hash import SHA256
from collections import namedtuple


class Block(namedtuple("BlockBaseClass", ("hash_pointer", "payload"))):
    def __hash__(self, genesis_block):
        sha = SHA256(self.hash_pointer)
        sha.update(self.payload)
        return sha.digest()

class BlockChain:

    #blocks contain tuples of the form (payload,sha256 of previous blocks payload
    #where each payload is a transaction, each transaction is a sequence of n ids, each followed by an amount
    #after which there is a sequence of the same n ids followed by different amounts
    #the first block "genesis block" is different, it has no hash and it's payload is
    #the title of the song "am I very wrong?" by Genesis

    def __init__(self,):
        self.blocks=[]
        self.blocks.append(('am I very wrong?',))

    def add_transaction(self,transaction):
        prev_block_payload=self.blocks[-1][0]
        myhash = SHA256.new(str.encode(prev_block_payload)).digest()
        self.blocks.append((transaction,myhash))

    def verify_integrity(self):
        prev_payload=self.blocks[0][0]
        for block in self.blocks[1:]:
            if not block[1] == SHA256.new(str.encode(prev_payload)).digest():
                return False
            prev_payload=block[0]
        return True

            


    


