import socket, select
import os
import hashlib


ZERO_BITS = 24


def _trailing_zero_count(some_bytes):
    # Dumb trailing zero bit counting
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


if __name__ == "__main__":
    try:
        with open("settings.txt", "r") as f:
            # Read settings from file
            # First argument is number of groups
            # Second argument is people per group
            GROUPS = int(f.readline())
            AMOUNT_OF_COMPETITORS = int(f.readline())*GROUPS
        print("Succeeded in reading from settings")
    except:
        print("Failed in reading from settings, resorting to defaults")
        GROUPS = 1
        AMOUNT_OF_COMPETITORS = 2*GROUPS

    PPG = AMOUNT_OF_COMPETITORS//GROUPS
    print("Starting a competition of", GROUPS, "groups with", PPG, "people in each group!")

    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 16  # Length of suffix
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(AMOUNT_OF_COMPETITORS)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

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
