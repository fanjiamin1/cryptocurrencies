import socket, select
from chat.crypto import RSA
from chat.misc.encoding_tools import ENCODING


RECEIVE_BUFFER_SIZE = 1024


class Peer:
    def __init__(self, port=None):
        self.RSA = RSA()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if port is not None:
            self.socket.bind(("", port))

    def set_public_key(self, key):
        self.RSA.set_public_key(key)

    def set_private_key(self, key):
        self.RSA.set_private_key(key)

    def send(self, address, message):
        encoded_message = bytes(message, ENCODING)
        encrypted_message = self.RSA.encrypt(encoded_message)
        self.socket.sendto(encrypted_message, address)

    def receive(self):
        encrypted_bytes = self.socket.recv(RECEIVE_BUFFER_SIZE)
        encoded_message = self.RSA.decrypt(encrypted_bytes)
        message = encoded_message.decode(ENCODING)
        return message

