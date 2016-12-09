import socket
import random
import threading
import time
import sys
from StoppableHashThread import StoppableHashThread
from Blockchain import Block, Blockchain
from io import StringIO
actual_stdout = sys.stdout
sys.stdout = StringIO()
from this import s as encrypted_this
sys.stdout = actual_stdout


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#port = random.randint(1000, 10000)
#address = ("127.0.0.1", port)
#s.bind(address)
#print("Running peer listening on address:", address)


# Build genesis block
# 32 bytes of padding+timestamp
genesis_payload = time.ctime(1000000000).zfill(Block.HASH_POINTER_SIZE).encode()
# Block.PAYLOAD_SIZE-32-32-1-16 bytes of documents+padding
genesis_payload += encrypted_this.encode().ljust(Block.PAYLOAD_SIZE - 32 - 32 - 1 - 16)
# 32 byte counter starting from zero
genesis_payload += bytes(32)
# 1 byte representing difficulty of work
genesis_payload += bytes([24])
# And then there is space of 16 bytes for nonce
genesis_payload += b"\x17"*16
print("---------------------------------------------")
print("GENESIS PAYLOAD (of length {}):".format(len(genesis_payload)))
print(genesis_payload)
print("---------------------------------------------")
genesis_block = Block(b"\x17"*Block.HASH_POINTER_SIZE, genesis_payload)


# Initialize blockchain with genesis block
blockchain = Blockchain(genesis_block)


#worker = StoppableHashThread()


# Broadcast test TODO Define function to broadcast?
s.sendto(b"Greetings!", ("<broadcast>", 54545))
print("Broadcasted greeting")


while True:
    pass
