import socket
import sys

from pychat.crypto import AES as Cipher


HOST = ""


class Bob:
    def __init__(self, port, key="0123456789defabc"):
        self.key = key
        self.cipher = Cipher(self.key)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, port))

    def start(self):
        try:
            while 1:
                print("Started listening...")
                self.socket.listen(2)
                connection, address = self.socket.accept()
                print("Incoming connection from", address)
                while 1:
                    data = connection.recv(1024)
                    if not data:
                        break
                    print("Alice:", self.cipher.decrypt(data))
                print("She hung up!")
        finally:
            connection.close()
            self.socket.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        port = int(input("Port: "))
        key = input("Encryption key: ")
    except KeyboardInterrupt:
        print()
        print("Can't get too hung up on Alice...")
        sys.exit()
    bob = Bob(port)  # key variable unused
    bob.start()
