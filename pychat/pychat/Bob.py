import socket
import sys
import hashlib


from .crypto import AES as Cipher
from .crypto.work import hash_work as work
from .misc.encoding_tools import ENCODING


HOST = ""


class Bob:
    def __init__(self, port, key="0123456789defabc"):
        self.key = key
        self.cipher = Cipher(self.key)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((HOST, port))

    def start(self):
        PREAMBLE = "!!!"
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
                    try:
                        data = self.cipher.decrypt(data)
                    except UnicodeDecodeError:
                        print(PREAMBLE, "Received gibberish from Alice", address)
                        continue
                    split_data = data.split(' ')
                    if len(split_data) == 3 and split_data[0] == "task:":
                        print(PREAMBLE, "Alice", address, " sent me a task!")
                        try:
                            print(PREAMBLE, "It looks like this:", split_data)
                            _, prefix, bits = split_data
                            bits = int(bits)
                            prefix = bytes(prefix, ENCODING)
                            print(PREAMBLE, "Prefix:", prefix)
                            print(PREAMBLE, "Difficulty:", bits)
                            suffix = work(prefix, bits)
                            print(PREAMBLE, "Found suffix:", suffix)
                            print(PREAMBLE
                                 , "sha256(prefix + suffix): ..."
                                 , hashlib.sha256(prefix + suffix).digest()[-10:]
                                 )
                        except:
                            print(PREAMBLE, "I failed at the task...")
                    else:
                        print("Alice {}:".format(address), data)
                print("She hung up!")
        finally:
            try:
                connection.close()
            except UnboundLocalError:
                pass
            self.socket.shutdown(socket.SHUT_RDWR)
            #self.socket.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        port = int(input("Port: "))
        key = input("Encryption key: ")
        bob = Bob(port, key=key) if key else Bob(port)
        bob.start()
    except (KeyboardInterrupt, EOFError):
        print()
        print("Can't get too hung up on Alice...")
        sys.exit()
    except:
        print("Bob is confused...")
        sys.exit()
