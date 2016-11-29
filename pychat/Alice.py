import socket
import sys


from .AES import AES as Cipher


class Alice():
    def __init__(self, key="0123456789defabc"):
        self.key = key
        self.cipher = Cipher(self.key)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip_address, port):
        self.socket.connect((ip_address, port))

    def send(self, message):
        self.socket.sendall(self.cipher.encrypt(message))


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        bob_ip = input("IP address: ")
        bob_port = int(input("Port: "))
        key = input("Encryption key: ")
    except KeyboardInterrupt:
        print()
        print("No chatting with Bob today... </3")
        sys.exit()
    print("Connecting to {} on port {}".format(bob_ip, bob_port))
    alice = Alice(key)
    try:
        alice.connect(bob_ip, bob_port)
    except:
        print("Couldn't get a connection with Bob...")
        sys.exit()
    try:
        while 1:
            alice.send(input("Message: "))
    except KeyboardInterrupt:
        print()
        print("That's enough chatting for now")
