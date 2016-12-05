import socket
import sys


from pychat.crypto import AES as Cipher
from Crypto import Random


class Alice():
    def __init__(self, key="0123456789defabc"):
        self.key = key
        self.cipher = Cipher(self.key)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip_address, port):
        self.socket.connect((ip_address, port))

    def send(self, message):
        self.socket.sendall(self.cipher.encrypt(message))

    def assign(self,difficulty=10, prefix='thisiseasymonkey'):
        print('in assign')
        self.send(prefix+' '+str(difficulty))
        #felt like this would do more...
        
        

        
        


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
        while 1:
            print("to send a proof of work task"
                 
                 +"simply write 'task', you can also specify"
                 +"a 16 byte prefix and a number of zeroes"
                 +"to be found in a sha5 hash with that prefix"
                 +"by writing task(prefix,numzeroes)")
            print("you can also send simple encrypted messages")

            message=input("Message: ")
            print(message)
            print(message.lower())
            print(message.lower()=='task')
            istask=False
            if message.lower()=='task':
                istask=True
                alice.assign()
            elif message.lower()[:5]=="task(":
                istask=True
                prefix=message[5:21]
                try:
                    difficulty=int(message[22:])
                except ValueError:
                    istask=False
                if istask:
                    alice.assign(prefix,difficulty)

            if not istask:
                alice.send(message)

    except KeyboardInterrupt:
        print()
        print("That's enough chatting for now")

