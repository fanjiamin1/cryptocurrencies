import socket
import sys
from pychat.crypto.work import hash_work as work




class Alice():
    def __init__(self, key="0123456789defabc"):
        self.key = key
        self.cipher = Cipher(self.key)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip_address, port):
        self.socket.connect((ip_address, port))

    def send(self, message):
        self.socket.sendall(message)


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
    print("Attempting to connect to {} on port {}".format(bob_ip, bob_port))
    alice = Alice()  # key variable unused
    try:
        alice.connect(bob_ip, bob_port)
    except:
        print("Couldn't get a connection with Bob...")
        sys.exit()
    try:
        read_sockets,write_sockets,select.select([alice.socket],[],[])
        for socket in read_sockets:
            message=socket.rcv(136)
            prefix=message[:128]
            difficulty=message[-1]
            suffix=work(prefix,difficulty)
            socket.send(suffix)
            


        #while 1:
            #alice.send(input("Message: "))
    except KeyboardInterrupt:
        print()
        print("That's enough chatting for now")

