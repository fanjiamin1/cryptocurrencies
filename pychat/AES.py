import Crypto.Cipher
from Crypto import Random
from pychat.misc.encoding_tools import ENCODING


class AES:
    def __init__(self, key):
        self.key = bytes(key, ENCODING)
        initilization_vector = Random.new().read(Crypto.Cipher.AES.block_size)
        self.cipher = Crypto.Cipher.AES.new(key,
                                            Crypto.Cipher.AES.MODE_ECB,
                                            initilization_vector)

    def salt(saltsize):
        salt = Random.new().read(size)
        return salt

    def encrypt(self, message):
        saltsize = 16 - len(message)
        pad = ' ' * saltsize
        pad_message = message + pad
        ciphertext = self.cipher.encrypt(message)
        ciphertext_salted = self.salt(saltsize) + ciphertext

        return ciphertext_salted
 
    def decrypt(self, message):
        padded_cleartext = self.cipher.decrypt(message).decode(ENCODING)
        saltsize = 16 - len(message)
        cleartext = padded_cleartext[-saltsize:]
        
        return cleartext
