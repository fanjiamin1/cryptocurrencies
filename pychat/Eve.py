import socket
import sys



HOST = ""


class Eve:
    def __init__(self,inport,outport,ip_address):
        self.insocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.insocket.bind((HOST, inport))
        self.outsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect(ip_address,outport)

    def connect(self, ip_address, port):
        self.outsocket.connect((ip_address, port))

    def send(self, message):
        self.outsocket.sendall(self.cipher.encrypt(message))
    
    #starts listening and transmitting
    def start(self):
        try:
            while 1:
                print("Started listening...")
                self.insocket.listen(2)
                connection, address = self.insocket.accept()
                print("Incoming connection from", address)
                while 1:
                    data = connection.recv(1024)
                    if not data:
                        break
                    outsocket.send(data)
                    #open socket to second client and send data
                print("Reflection complete")
        finally:
            try:
                connection.close()
            except UnboundLocalError:
                pass
            self.socket.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) !=0 and args[0] in ['help','-help','h','-h']:
        print("\n This program takes 3 arguments, example call: python Eve.py in out ip \n"
               +"the program listens for traffic on the port 'in' and transmits any data recieved \n"
               +"to the ip address 'ip' on the port 'out'")
        sys.exit(1)
    try:
        if len(args)==3:
            inport=int(args[0])
            outport=int(args[1])
            target_ip=args[2]
        else:
            inport = int(input("Receiving Port: "))
            outport = int(input("Transmitting Port: "))
            target_ip = (input("Target IP address: "))
        eve = Eve(inport,outport,target_ip)  # key variable unused
        eve.start()
        print('starting the looking glass')
    except KeyboardInterrupt:
        print()
        print('We are now beyond the looking glass')
        sys.exit()
