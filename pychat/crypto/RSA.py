import Crypto.PublicKey.RSA
from pychat.crypto import Cipher
from pychat.misc.encoding_tools import ENCODING


class RSA(Cipher):
    def __init__(self, key):
        self._key = Crypto.PublicKey.RSA.importKey(key)

    @staticmethod
    def generate_key(strength=0):
        bits = 1024 + strength*256
        return Crypto.PublicKey.RSA.generate(bits).exportKey()

    def encrypt(self, cleartext):
        ciphertext, = self._key.encrypt( 
                                         bytes(cleartext, ENCODING)
                                       , b"Unused argument"
                                       )
        return ciphertext

    def decrypt(self, ciphertext):
        return self._key.decrypt(ciphertext).decode(ENCODING)
