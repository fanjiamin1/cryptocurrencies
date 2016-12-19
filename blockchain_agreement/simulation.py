import threading
import time
import sys
import os
import pickle
import collections
import random
from hashlib import sha256 as Hash
from Blockchain import Block, Blockchain


# Try to import curses
try:
    import curses
    CURSES = True
except ImportError:
    CURSES = False


# Import "rot 13 this" without printing to stdout
from io import StringIO
actual_stdout = sys.stdout
sys.stdout = StringIO()
from this import s as rot_13_this
sys.stdout = actual_stdout


#
# Simulation specific Block and Blockchain inheriting from generic implementations
#


class SimulationBlock(Block):
    FILL_CHARACTER = b"#"
    def __init__(self, hash_pointer, time, document, counter, difficulty, nonce):
        payload = SimulationBlock.join_components(
                                                   time
                                                 , document
                                                 , counter
                                                 , difficulty
                                                 , nonce
                                                 )
        super(SimulationBlock, self).__init__(hash_pointer, payload)

    @classmethod
    def genesis_block(cls):
        hash_pointer = b"\x17"*cls.HASH_POINTER_SIZE
        genesis_time = time.ctime(1000198000).encode()
        document = rot_13_this.encode()
        # 32 byte counter starting from zero
        counter = bytes(32)
        # 1 byte representing difficulty of work
        difficulty = bytes([DIFFICULTY])
        # And then there is space of 16 bytes for nonce
        nonce = b"\x17"*16
        return cls(hash_pointer, genesis_time, document, counter, difficulty, nonce)

    @staticmethod
    def join_components(time, document, counter, difficulty, nonce):
        time = time.ljust(
                           SimulationBlock.HASH_POINTER_SIZE
                         , SimulationBlock.FILL_CHARACTER
                         )
        genesis_payload += rot_13_this.encode()
        # 32 byte counter starting from zero
        genesis_payload += bytes(32)
        # 1 byte representing difficulty of work
        genesis_payload += bytes([DIFFICULTY])
        # And then there is space of 16 bytes for nonce
        genesis_payload += b"\x17"*16
        genesis_block = Block(b"\x17"*Block.HASH_POINTER_SIZE, genesis_payload)

    @staticmethod
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

    @staticmethod
    def counter_value(byte_array_counter):
        result = 0
        for b in byte_array_counter:
            result <<= 8  # Byte size
            result += b
        return result


class SimulationBlockchain(Blockchain):
    def pretty(self):
        """Method that gives a slightly "pretty printed" string representation."""
        result = ["SimulationBlockchain at {}\n".format(id(self))]
        index = 0
        for block in self:
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


# TODO: Integrate into Miner
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


class Simulation(threading.Thread):
    STR = "Simulation of {:d} miners:\n\tDifficulty {:d}\n\tMessage interference rate: {:f}"
    def __init__(self, total_miners, difficulty, interference_rate=0.1):
        self.total_miners = total_miners
        self.difficulty = difficulty
        self.miners = []
        for id_number in range(self.total_miners):
            self.miners.append(Miner(id_number))

        # Communication variables
        self.broadcast_lock = threading.RLock()
        self.broadcast_count = 0
        self.interfered_count = 0
        self.interference_rate = interference_rate

    def __str__(self):
        return Simulation.STR.format(self.total_miners, self.difficulty, self.interference_rate)

    def run(self):
        # Broadcast genesis blockchain without interference
        broadcast(pickle.dumps(blockchain), interference=False)

        # Starting line for miners
        self.starting_line = threading.Barrier(total_miners + 1)

        # Start miners
        for miner in self.miners:
            miner.start()

        starting_line.wait()  # Start mining once all miners ready

        while True:
            pass  # Curses graphix yo

    def broadcast(self, message_bytes, exclude=None, interference=True):
        with self.broadcast_lock:
            for miner in self.miners:
                if miner == exclude:
                    continue
                elif interference and random.randint(0, 100) <= 100*self.interference_rate:
                    # Use random to determine whether or not to "accidentally" drop message
                    miner.messages_lost += 1
                    self.interference_count += 1
                else:
                    miner.send_message(message_bytes)
            self.broadcast_count += 1


def main_curses(stdscr, total_miners, difficulty):
    # Clear screen
    stdscr.clear()

    # Hide cursor
    curses.curs_set(False)

    # Create simulation

    simulation = Simulation(total_miners, difficulty)
    stdscr.addstr(0, 0, str(simulation))
    stdscr.refresh()
    time.sleep(4)


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        assert len(args) == 2
        total_miners = int(args[0])
        difficulty = int(args[1])
    except:
        print("Usage: {} total_miners difficulty".format(sys.argv[0]))
        sys.exit()

    if CURSES:
        curses.wrapper(main_curses, total_miners, difficulty)
        sys.exit()
    else:
        print("curses library not present")
        sys.exit()


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

    # Display miners' progress
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
        miner.join()
