import socket, select
import os
import hashlib
import configparser


RECV_BUFFER = 16  # Length of suffix


def _trailing_zero_count(some_bytes):
    """Dumb trailing zero bit counting."""
    bit_str = bin(int(some_bytes.hex(), 16))
    return len(bit_str) - len(bit_str.rstrip('0'))


#Function to broadcast chat messages to all connected clients
def broadcast_data (message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket:
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)


class UDPServer:
    def __init__(self, host, port, groups, people):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server
    def __enter__(self):
        print("ENTER")
        pass
    def __exit__(self):
        print("EXIT")
        pass


if __name__ == "__main__":
    print("Proof of work competition!")
    try:
        config = configparser.ConfigParser()
        config.sections()
        config.read("config.cfg")
        rounds = config["Competition"].getint("rounds")
        groups = config["Competition"].getint("groups")
        people = config["Competition"].getint("people")
        bits = config["Challenge"].getint("bits")
        protocol = config["Networking"]["protocol"]
        host = config["Networking"]["host"]
        port = config["Networking"]["port"]
    except:
        print("Unable to load config file")
        print("Falling back on defaults")
        groups = 2
        people = 1
        rounds = 32
        bits = 27
        protocol = "UDP"
        host = "0.0.0.0"
        port = 8888
    print("Networking details:")
    print("\tProtocol:", protocol)
    print("\tHost:", host)
    print("\tPort:", port)
    print("Competition details:")
    print("\tRounds:", rounds)
    print("\tGroups:", groups)
    print("\tPeople:", people)
    print("Challenge details:")
    print("\tType: Trailing zero hashing")
    print("\tBits:", bits)
    if protocol == "UDP":
        Server = UDPServer
    elif protocol == "TCP":
        Server = TCPServer
    else:
        print("Unrecognized protocol")
    with Server(host, port, groups*people) as server:
        print("With server object")
        for round_number in range(1, rounds+1):
            print("ROUND", round_number)


class TCPServer:
    def __init__(self, host, port, competitors):
        # List to keep track of socket descriptors
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(competitors)
        self.connection_list = [server_socket]


if False:#__name__ == "__main__":


    # Add server socket to the list of readable connections

    print("Competition server started on port " + str(PORT))

    while True:
        if len(CONNECTION_LIST) - 1 == AMOUNT_OF_COMPETITORS:
            print("Got {} participants!".format(AMOUNT_OF_COMPETITORS))
            break
        else:
            print("We have {} participants so far".format(len(CONNECTION_LIST) - 1))

        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print("Competitor {} connected".format(addr))

    print("Let the games begin!")
    prefix = os.urandom(16)
    challenge_message = prefix + bytes([ZERO_BITS])
    print("")
    print("The challenge is to find {} for:".format(ZERO_BITS))
    print("\t{}".format(prefix))
    print("")
    broadcast_data(challenge_message)
    success = False
    while not success:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST,[],[])
        for sock in read_sockets:
            addr = sock.getpeername()
            #New connection
            if sock == server_socket:
                pass  # Ignore connections
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    suffix = sock.recv(RECV_BUFFER)
                except:
                    print("Error for {}! Closing connection".format(addr))
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
                # Check if challenge completed
                digest = hashlib.sha256(prefix + suffix).digest()
                bin_repr = tuple(map(lambda x: bin(x)[2:].zfill(8), digest))
                count = _trailing_zero_count(digest)
                success = count >= ZERO_BITS
                print("Got suffix:")
                print("\t", suffix)
                print("from {} which gives hash".format(addr))
                print("\t...")
                slice_index = -((count//8)+1) if count < 249 else 0
                for chomp in bin_repr[slice_index:]:
                    print("\t{}".format(chomp))
                if success:
                    print("WINNER! {} with {} zero bits!".format(addr, count))
                    print("Game over")
                else:
                    print("which has {} zero bits...".format(count))
                    print("WRONG {}! Closing connection".format(addr))
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                if success:
                    break

    server_socket.close()  # Eh...
