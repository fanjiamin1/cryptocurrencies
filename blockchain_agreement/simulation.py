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


# Milliseconds since epoch function that might not be portable
def get_ms_since_epoch():
    return int(time.time()*1000)


class Slave(threading.Thread):
    """A slave thread that looks for a nonce that gives difficulty-many zero bits."""
    def __init__(self, master, base_hash, difficulty):
        self.master = master
        self.difficulty = difficulty
        self.base_hash = base_hash

        # Other attributes
        self.stopped = False
        self.result = None

        super(Slave, self).__init__()

    def run(self):
        while not self.stopped:
            nonce, digest = self._hash()
            if self._trailing_zero_count(digest) >= self.difficulty:
                self.result = (nonce, digest)
                self.master.notify()
                return

    def stop(self):
        self.stopped = True

    def _hash(self):
        temp_hash = self.base_hash.copy()
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


class Miner(threading.Thread):
    def __init__(self, id_number, supervisor):
        self.id_number = id_number
        self.supervisor = supervisor
        self.mailbox = collections.deque()
        self.mailbox_lock = threading.Lock()
        self.notification = threading.Event()
        self.stopped = False
        super(Miner, self).__init__()

    def run(self):
        # Get initial blockchain from mailbox
        self.blockchain = pickle.loads(self.read_mail())

        # Construct miner payload comment
        comment = "I, miner number {:d}, did this!".format(self.id_number)

        # Wait for supervisor's go signal
        self.supervisor.starting_line.wait()

        # Start mining!
        while True:

            # Create new block miner wants on chain

            # Get latest block
            latest_block = self.blockchain.latest_block
            # Create hash pointer for block
            hash_pointer = latest_block.hash()
            # Get milliseconds for block
            time_stamp = get_ms_since_epoch()
            # At this point the comment should be gotten, but it has already been made
            # comment = comment
            # Get new counter by incrementing old counter
            new_counter = latest_block.counter + 1
            # Get difficulty from latest block
            difficulty = latest_block.difficulty
            # Get nonce, but it is not known yet!
            no_nonce = b""

            # Calculate base hash
            no_nonce_block = Block(
                                    hash_pointer
                                  , time_stamp
                                  , comment
                                  , new_counter
                                  , difficulty
                                  , no_nonce
                                  )
            base_hash = no_nonce_block.hash()

            # Create new slave to find good nonce
            self.slave = Slave(self, base_hash, difficulty)
            self.slave.start()

            while True:
                # Wait for notification from:
                #  - Slave having found nonce
                #  - Supervisor stopping the "gold rush"/mining
                #  - Other miners sending messages
                self.wait()

                # Waiting on notifications
                # Check if supervisor announced stop
                if self.stopped:
                    break

            # Do some work that the slave can't be trusted to do
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
        self.notify()

    def mail(self, message_bytes):
        with self.mailbox_lock:
            self.mailbox.append(message_bytes)
            self.notify()

    def has_mail(self):
        # False if mailbox is empty, else True
        return bool(self.mailbox)

    def read_mail(self):
        with self.mailbox_lock:
            return self.mailbox.popleft()

    def notify(self):
        self.notification.set()

    def wait(self):
        # Wait for notification
        self.notification.wait()
        # Clear notification flag
        # It matters not if it is set in the meantime
        self.notification.clear()


class Simulation(threading.Thread):
    STR = "Simulation of {:d} miners:\nDifficulty: {:d}\nMessage interference rate: {:f}"
    def __init__(self, total_miners, difficulty, interference_rate=0.1):
        self.total_miners = total_miners
        self.difficulty = difficulty
        self.miners = []
        for id_number in range(self.total_miners):
            self.miners.append(Miner(id_number, self))

        # Communication variables
        self.broadcast_lock = threading.RLock()
        self.broadcast_count = 0
        self.interfered_count = 0
        self.interference_rate = interference_rate

        # Thread running variables
        self.stop_event = threading.Event()

    def __str__(self):
        return Simulation.STR.format(self.total_miners, self.difficulty, self.interference_rate)

    def run(self):
        # Broadcast genesis blockchain without interference
        block = Block.genesis_block(self.difficulty)
        blockchain = Blockchain(block)
        self.broadcast(pickle.dumps(blockchain), interference=False)

        # Starting line for miners
        self.starting_line = threading.Barrier(total_miners + 1)

        # Start miners
        for miner in self.miners:
            miner.start()

        self.starting_line.wait()  # Start mining once all miners ready

        self.stop_event.wait()


    def stop(self):
        self.stop_event.set()
        for miner in self.miners:
            miner.stop()
            miner.join()

    def broadcast(self, message_bytes, exclude=None, interference=True):
        with self.broadcast_lock:
            for miner in self.miners:
                if miner == exclude:
                    continue
                elif interference and random.randint(0, 100) <= 100*self.interference_rate:
                    # Use random to determine whether or not to "accidentally" drop message
                    self.interference_count += 1
                else:
                    miner.mail(message_bytes)
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

    try:
        simulation.run()
    except KeyboardInterrupt:
        stdscr.clear()
        stdscr.addstr(0, 0, "Halting simulation...")
        stdscr.refresh()
        simulation.stop()


def main_no_curses(total_miners, difficulty):
    simulation = Simulation(total_miners, difficulty)
    print(simulation)
    try:
        simulation.run()
    except KeyboardInterrupt:
        simulation.stop()


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
        #curses.wrapper(main_curses, total_miners, difficulty)
        main_no_curses(total_miners, difficulty)
    else:
        main_no_curses(total_miners, difficulty)


    sys.exit()

    # TODO: Implement the below code into non-curses displaying

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
