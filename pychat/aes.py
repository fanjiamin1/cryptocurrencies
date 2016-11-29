import Crypto.Cipher
from Crypto import Random
from pychat.misc import ENCODING


class AES:
    def __init__(self, key):
        self.key = bytes(key, ENCODING)
        initilization_vector = Random.new().read(Crypto.Cipher.AES.block_size)
        self.cipher = Crypto.Cipher.AES.new(key,
                                            Crypto.Cipher.AES.MODE_ECB,
                                            initilization_vector)

    def encrypt(self, message):
        return self.cipher.encrypt(message)
 
    def decrypt(self, message):
        return self.cipher.decrypt(message).decode(ENCODING)
