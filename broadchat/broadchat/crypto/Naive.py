from pychat.misc.encoding_tools import ENCODING
from pychat.crypto import Cipher


class Naive(Cipher):
    def __init__(self, key):
        self.key = key

    def encrypt(self, cleartext):
        ciphertext = bytes(byte^self.key for byte in bytes(cleartext, ENCODING))
        return ciphertext
    
    def decrypt(self, ciphertext):
        cleartext = bytes(byte^self.key for byte in ciphertext).decode(ENCODING)
        return cleartext
