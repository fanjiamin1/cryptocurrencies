import socket
import random
import threading
import time
import sys
import os
import pickle
import collections
from hashlib import sha256 as Hash
from Blockchain import Block, Blockchain


# Import rot 13 this without printing to stdout
from io import StringIO
actual_stdout = sys.stdout
sys.stdout = StringIO()
from this import s as rot_13_this
sys.stdout = actual_stdout


DOCSIZE = Block.PAYLOAD_SIZE - 32 - 32 - 1 - 16


# Build genesis block
# 32 bytes of padding+timestamp
genesis_payload = time.ctime(1000198000).zfill(Block.HASH_POINTER_SIZE).encode()
# Block.PAYLOAD_SIZE-32-32-1-16 bytes of documents+padding
genesis_payload += rot_13_this.encode().ljust(DOCSIZE)
# 32 byte counter starting from zero
genesis_payload += bytes(32)
# 1 byte representing difficulty of work
genesis_payload += bytes([24])
# And then there is space of 16 bytes for nonce
genesis_payload += b"\x17"*16
#print("---------------------------------------------")
#print("GENESIS PAYLOAD (of length {}):".format(len(genesis_payload)))
#print(genesis_payload)
#print("---------------------------------------------")
genesis_block = Block(b"\x17"*Block.HASH_POINTER_SIZE, genesis_payload)


# The genesis block chain
blockchain = Blockchain(genesis_block)


# Communication variables
communication_lock = threading.Lock()
sockets = []
miner_ids = []
miners = []


def broadcast(byte_array):
    with communication_lock:
        for socket in sockets:
            socket.append(byte_array)

def read_socket(miner_id):
    try:
        with communication_lock:
            return sockets[miner_id].popleft()
    except IndexError:
        return None


class Thrall(threading.Thread):
    def __init__(self, latest_block, payload):
        # Prehash
        hash_ptr = Hash()
        hash_ptr.update(latest_block.hash_pointer)
        hash_ptr.update(latest_block.payload)
        self.prehash = Hash()
        self.prehash.update(hash_ptr.digest())
        self.prehash.update(time.ctime().zfill(Block.HASH_POINTER_SIZE).encode())
        self.prehash.update(payload.zfill(DOCSIZE))
        old_counter = latest_block.payload[-17-32:-17]
        assert len(old_counter) == 32
        self.prehash.update(old_counter)  # TODO
        difficulty = latest_block.payload[-16-1:-16]
        assert len(difficulty) == 1
        assert difficulty[0] == 24
        self.difficulty = difficulty[0]
        self.prehash.update(difficulty)

        # Other attributes
        self.stopped = False
        self.found = False
        self.result = None

        super(Thrall, self).__init__()

    def stop(self):
        self.stopped = True

    def hash(self):
        temp_hash = self.prehash.copy()
        nonce = os.urandom(16)
        temp_hash.update(nonce)
        digest = temp_hash.digest()
        return nonce, digest

    def _trailing_zero_count(self, some_bytes):
        # Dumb trailing zero bit counting... stupid Thrall
        bit_str = bin(int(some_bytes.hex(), 16))
        return len(bit_str) - len(bit_str.rstrip('0'))

    def run(self):
        while not self.stopped:
            nonce, digest = self.hash()
            if self._trailing_zero_count(digest) >= self.difficulty:
                self.result = (nonce, digest)
                self.found = True
                return


class Miner(threading.Thread):
    def __init__(self, id_number):
        self.id_number = id_number
        super(Miner, self).__init__()

    def run(self):
        while True:
            message = read_socket(self.id_number)
            if message is None:
                continue
            else:
                blockchain = pickle.loads(message)
                if not isinstance(blockchain, Blockchain):
                    print("Surprising junk on mah socket, bby")
                    continue
                self.blockchain = blockchain
                break
        payload = b"I, miner number "
        payload += bytes([ord(str(self.id_number))])
        payload += b" did this!"
        while True:
            # Create new slave to find good nonce
            self.slave = Thrall(blockchain.latest_block, payload)
            self.slave.start()
            while True:
                if self.slave.found is True:
                    # Found nonce! Should try to get block on chain!
                    break
                else:
                    # Did not find good nonce yet...
                    pass
                if sockets[self.id_number]:
                    # Some message waiting on socket! Should read
                    pass
                else:
                    # No messages for miner...
                    pass
            print(self.slave.result)
            # Kill slave despite his efforts
            self.slave.join()
            break


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit()
    try:
        total_miners = int(args[0])
    except:
        sys.exit()

    # Create miners
    for miner_id in range(total_miners):
        print("Creating miner", miner_id)
        sockets.append(collections.deque())
        miner_ids.append(miner_id)
        miners.append(Miner(miner_id))

    # Broadcast block
    print("Broadcasting genesis block in a single block blockchain")
    broadcast(pickle.dumps(blockchain))

    # Start miners
    for miner_id in miner_ids:
        print("Starting miner", miner_id)
        miners[miner_id].start()

    for miner in miners:
        miner.join()
