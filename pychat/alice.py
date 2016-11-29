import socket
import sys
import pychat


class Alice():
    def __init__(self):
        self.key = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip_address, port):
        self.socket.connect((ip_address, port))

    def send(self, message):
        bob_socket.sendall(pychat.encrypt(self.key, message))


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        bob_ip = input("IP address: ")
        bob_port = int(input("Port: "))
        key = int(input("Encryption key: "))
    except KeyboardInterrupt:
        print()
        print("No chatting with Bob today... </3")
        sys.exit()
    print("Connecting to {} on port {}".format(bob_ip, bob_port))
    alice = Alice()
    alice.key = key
    alice.connect(bob_ip, bob_port)
    while 1:
        alice.send(input("Message: "))
