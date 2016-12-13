import socket
import random
import threading
import time
import sys
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


# Build genesis block
# 32 bytes of padding+timestamp
genesis_payload = time.ctime(1000198000).zfill(Block.HASH_POINTER_SIZE).encode()
# Block.PAYLOAD_SIZE-32-32-1-16 bytes of documents+padding
genesis_payload += rot_13_this.encode().ljust(Block.PAYLOAD_SIZE - 32 - 32 - 1 - 16)
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


class MinerDelegate(threading.Thread):
    def __init__(self,block_contents,target):
        #accepts blocks in the form of a list of strings
        #each of which is a field of the previous block
        super(StoppableThread,self).__init__()
        self.stopped=False
        self.prehash=SHA()

        self.nonce=0
        for item in block_contents:
            self.prehash.update(str.encode(item))

        self.found=False

    def stop(self):
        self.stopped=True

    def myhash(self):
        #steal this from proofofwork
        temphash=self.prehash.copy()
        temphash.update(str.encode(str(self.nonce)))
        self.nonce+=1
        return temphash.digest()

    def run(self):
        while not stopped:
            guess=hash()
            if myHash[0:len(target)] == target:
                self.found=True
                return


def broadcast(byte_array):
    with communication_lock:
        for socket in sockets:
            socket.append(byte_array)

def read_socket(miner_id):
    try:
        return sockets[miner_id].popleft()
    except IndexError:
        return None


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit()
    try:
        miners = int(args[0])
    except:
        sys.exit()

    for number in range(miners):
        sockets.append(collections.deque())
        print("Creating miner", number)
        miner_ids.append(number)

    print("Broadcasting genesis block in a single block blockchain")
    broadcast(pickle.dumps(blockchain))

    for miner_id in miner_ids:
        print("Starting miner", miner_id)

    for miner_id in miner_ids:
        while True:
            message = read_socket(miner_id)
            if message is None:
                print("Miner", miner_id, "received nothing")
                break
            else:
                print("Miner", miner_id, "received something!")
