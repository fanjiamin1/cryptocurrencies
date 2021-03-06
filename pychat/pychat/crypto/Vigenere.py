from pychat.misc.encoding_tools import char2byte, byte2char
from pychat.misc.encoding_tools import ENCODING, MAX_BYTE
from pychat.crypto import Cipher


class Vigenere(Cipher):
    def __init__(self, key):
        self.key = [char2byte(character) for character in key]

    def encrypt(self, message):
        message = [char2byte(character) for character in message]
        for index in range(len(message)):
            message[index] += self.key[index % len(self.key)]
            message[index] %= MAX_BYTE
        return bytes(message)

    def decrypt(self, message):
        message = list(message)
        for index in range(len(message)):
            message[index] -= self.key[index % len(self.key)]
            message[index] %= MAX_BYTE
        return "".join(byte2char(character) for character in message)
