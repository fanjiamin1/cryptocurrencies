import Crypto.PublicKey.RSA
from chat.misc.encoding_tools import ENCODING


class RSA:
    def __init__(self, key):
        self._key = Crypto.PublicKey.RSA.importKey(key)

    @staticmethod
    def generate_key(strength=0):
        bits = 1024 + strength*256
        return Crypto.PublicKey.RSA.generate(bits).exportKey()

    def encrypt(self, cleartext_bytes):
        ciphertext_bytes, = self._key.encrypt( 
                                               cleartext_bytes
                                             , b"Unused argument"
                                             )
        return ciphertext_bytes

    def decrypt(self, ciphertext_bytes):
        return self._key.decrypt(ciphertext_bytes)
