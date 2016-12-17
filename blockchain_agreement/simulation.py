import threading
import time
import sys
import os
import pickle
import collections
from hashlib import sha256 as Hash
from Blockchain import Block, Blockchain


# Import "rot 13 this" without printing to stdout
from io import StringIO
actual_stdout = sys.stdout
sys.stdout = StringIO()
from this import s as rot_13_this
sys.stdout = actual_stdout


FILLCHAR = b"#"
DOCSIZE = Block.PAYLOAD_SIZE - 32 - 32 - 1 - 16
DIFFICULTY = None
PREAMBLE = "Simulation of {} miners with difficulty {}"
INTERFERENCE_EVERY = 2  # Drop a message from a socket every n-th time a miner attempts to read a message
BROADCAST_INTERFERE_EVERY = 4  # Same but broadcasts


# Communication variables
communication_lock = threading.RLock()
sockets = []
miner_ids = []
miners = []
read_counter = 0
broadcast_counter = -1


refresh_flag = threading.Event()
interference_flag = threading.Event()
interfered = []  # total interfered messages


#
# Blockchain or block related functions and variables
#


def pretty_blockchain(bc):
    """Function that does a slightly "pretty printed" string repr of a blockchain."""
    result = ["Blockchain at {}\n".format(id(bc))]
    index = 0
    for block in bc:
        result.append("\t")
        result.append("Block {}\n".format(index))
        result.append("\t\t")
        result.append(repr(block.hash_pointer[:16]))
        result.append("...\n")
        result.append("\t\t")
        result.append(repr(block.payload[:32]))
        result.append("...\n")
        index += 1
    return "".join(result)


def increment_counter(byte_array_counter):
    index = -1
    while True:
        try:
            byte_array_counter[index] += 1
            return
        except ValueError:
            byte_array_counter[index] = 0
            index -= 1
        except IndexError:
            # Counter overflow!
            for i in range(byte_array_counter):
                byte_array_counter[i] = 0
            return


def counter_value(byte_array_counter):
    result = 0
    for b in byte_array_counter:
        result <<= 8  # Byte size
        result += b
    return result


#
# Thread communication functions and variables
#


def broadcast(own_miner_id, byte_array):
    global broadcast_counter
    with communication_lock:
        if broadcast_counter >= BROADCAST_INTERFERE_EVERY:
            broadcast_counter = 0
            for miner_id in miner_ids:
                interfered[miner_id] += 1
        else:
            for miner_id in miner_ids:
                if miner_id == own_miner_id:
                    continue
                sockets[miner_id].append(byte_array)
            broadcast_counter += 1


def read_socket(miner_id):
    global read_counter
    try:
        with communication_lock:
            message = sockets[miner_id].popleft()
            read_counter += 1
            if read_counter >= INTERFERENCE_EVERY:
                read_counter = 0
                interfered[miner_id] += 1
                return None
            else:
                return message
    except IndexError:
        return None


#
# A miner, and his slave (Thrall) that is sent to do work
#


class Thrall(threading.Thread):
    def __init__(self, hash_ptr_digest, prehash_components, difficulty):
        self.difficulty = difficulty

        # Prehash
        self.prehash = Hash(hash_ptr_digest)
        filter(self.prehash.update, prehash_components)

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
        index = 1
        total = 0
        mask = 1
        while True:
            b = some_bytes[-index]
            if b == 0:
                total += 8
                if index == len(some_bytes):
                    return total
                index += 1
            else:
                for value in range(8):
                    if b & mask != 0:
                        total += value
                        return total
                    else:
                        mask *= 2

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
        self.stopped = False
        super(Miner, self).__init__()

    def run(self):
        while True:
            message = read_socket(self.id_number)
            if message is None:
                continue
            else:
                self.blockchain = pickle.loads(message)
                if not isinstance(self.blockchain, Blockchain):
                    print("Surprising junk on mah socket, bby")
                    continue
                break
        barrier.wait()
        payload_comment = b"I, miner number "
        payload_comment += bytes([ord(str(self.id_number))])
        payload_comment += b" did this!"
        payload_comment = payload_comment.ljust(DOCSIZE, FILLCHAR)
        while not self.stopped:
            # Do some work that the slave can't be trusted to do
            latest_block = self.blockchain.latest_block
            hash_ptr = Hash()
            hash_ptr.update(latest_block.hash_pointer)
            hash_ptr.update(latest_block.payload)
            payload_components = []
            payload_components.append(time.ctime().encode().ljust(Block.HASH_POINTER_SIZE, FILLCHAR))
            payload_components.append(payload_comment)
            old_counter = latest_block.payload[-17-32:-17]
            assert len(old_counter) == 32
            payload_components.append(old_counter)  # TODO
            difficulty = latest_block.payload[-16-1:-16]
            assert len(difficulty) == 1
            assert difficulty[0] == DIFFICULTY
            payload_components.append(difficulty)
            # Create new slave to find good nonce
            self.slave = Thrall(hash_ptr.digest(), payload_components, difficulty[0])
            self.slave.start()
            while True:
                if self.stopped:
                    break
                if sockets[self.id_number]:
                    # Some message waiting on socket! Should read
                    message = read_socket(self.id_number)
                    if message is None:
                        continue
                    received_blockchain = pickle.loads(message)
                    try:
                        received_blockchain.verify()
                        if received_blockchain.genesis_block != self.blockchain.genesis_block:
                            raise RuntimeError  # lol
                    except RuntimeError:
                        print("Miner", self.id_number, "received bogus blockchain")
                        continue
                    if len(received_blockchain) > len(self.blockchain):
                        assert self.blockchain != received_blockchain
                        self.blockchain = received_blockchain
                        refresh_flag.set()
                        break
                    else:
                        # Ignore smaller blockchain; size matters!
                        pass
                else:
                    pass  # No messages for miner...
                if self.slave.found is True:
                    # Found nonce! Should try to get block on chain!
                    self.slave.stop()
                    nonce = self.slave.result[0]
                    payload_components.append(nonce)
                    payload = b"".join(payload_components)
                    if len(payload) != Block.PAYLOAD_SIZE:
                        print(len(nonce))
                        print(len(payload))
                        print(payload)
                        print("Component lengths:")
                        for c in payload_components:
                            print("\t", len(c), ":", c)
                    self.blockchain.append(payload)
                    broadcast(self.id_number, pickle.dumps(self.blockchain))
                    refresh_flag.set()
                    break
                else:
                    pass  # Did not find good nonce yet...
            # Kill slave despite his efforts
            self.slave.stop()
            self.slave.join()

    def stop(self):
        self.stopped = True


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        sys.exit()
    try:
        total_miners = int(args[0])
        DIFFICULTY = int(args[1])
    except:
        sys.exit()

    # Build genesis block
    # 32 bytes of padding+timestamp
    genesis_payload = time.ctime(1000198000).encode().ljust(Block.HASH_POINTER_SIZE, FILLCHAR)
    # Block.PAYLOAD_SIZE-32-32-1-16 bytes of documents+padding
    genesis_payload += rot_13_this.encode().ljust(DOCSIZE, FILLCHAR)
    # 32 byte counter starting from zero
    genesis_payload += bytes(32)
    # 1 byte representing difficulty of work
    genesis_payload += bytes([DIFFICULTY])
    # And then there is space of 16 bytes for nonce
    genesis_payload += b"\x17"*16
    #print("---------------------------------------------")
    #print("GENESIS PAYLOAD (of length {}):".format(len(genesis_payload)))
    #print(genesis_payload)
    #print("---------------------------------------------")
    genesis_block = Block(b"\x17"*Block.HASH_POINTER_SIZE, genesis_payload)

    # Build the genesis block chain
    blockchain = Blockchain(genesis_block)

    # Barrier for miners
    barrier = threading.Barrier(total_miners+1)
    read_counter -= total_miners + 3

    # Create miners
    for miner_id in range(total_miners):
        #print("Creating miner", miner_id)
        sockets.append(collections.deque())
        interfered.append(0)
        miner_ids.append(miner_id)
        miners.append(Miner(miner_id))

    # Broadcast block
    #print("Broadcasting genesis block in a single block blockchain")
    broadcast(-1, pickle.dumps(blockchain))

    # Start miners
    for miner_id in miner_ids:
        #print("Starting miner", miner_id)
        miners[miner_id].start()

    barrier.wait()

    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            screen = []
            screen.append(PREAMBLE.format(total_miners, DIFFICULTY))
            screen.append("\n")
            N = 24
            slice_index = max(len(bcs.blockchain) for bcs in miners) - N
            for miner_id in miner_ids:
                mbc = miners[miner_id].blockchain[(0 if slice_index < 0 else slice_index):]
                screen.append(str(miner_id))
                screen.append(": ")
                for block in mbc:
                    screen.append("[")
                    screen.append(repr(block.hash_pointer[0]%10))
                    screen.append("]")
                screen.append("\n")
            screen.append("Interfered messages:")
            screen.append("\n")
            for miner_id in miner_ids:
                screen.append(str(miner_id))
                screen.append(": ")
                screen.append(str(interfered[miner_id]).rjust(4, " "))
                screen.append("\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            print("".join(screen))
            refresh_flag.wait()
            refresh_flag.clear()
    except:
        print()
        print("Simulation over, stopping participants")

    for miner in miners:
        miner.stop()
    for miner in miners:
        #with open("result-"+time.ctime()+".txt", "a") as f:
        #    f.write(pretty_blockchain(miner.blockchain))
        miner.join()
