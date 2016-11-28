import socket
import sys
import pychat

def alice():
    try:
        bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bob_ip = input("IP address: ")
        bob_port = int(input("Socket: "))
        key = int(input("Encryption key: "))
        print("Connecting to {} on socket {}".format(repr(bob_ip), repr(bob_port)))
        bob_socket.connect((bob_ip, bob_port))
    except:
        print("No good")
        raise
    print("Connected!")
    while 1:
        bob_socket.sendall(pychat.encrypt(key, input("Message: ")))
