import Crypto.PublicKey.RSA


class RSA:
    def __init__(self):
        self._public_key = None
        self._private_key = None

    @staticmethod
    def generate_key_pair(strength=0):
        bits = 1024 + strength*256
        private = Crypto.PublicKey.RSA.generate(bits)
        public = private.publickey()
        return (public, private)

    @staticmethod
    def key_to_file(file_name, key):
        with open(file_name, "wb") as key_file:
            key_file.write(key.exportKey())

    @staticmethod
    def key_from_file(file_name):
        with open(file_name, "rb") as key_file:
            key = key_file.read()
            return Crypto.PublicKey.RSA.importKey(key)

    def set_public_key(self, key):
        self._public_key = key

    def set_private_key(self, key):
        self._private_key = key

    def encrypt(self, cleartext_bytes, key=None):
        if key is None:
            key = self._public_key
        ciphertext_bytes, = key.encrypt( 
                                         cleartext_bytes
                                       , b"Unused argument"
                                       )
        return ciphertext_bytes

    def decrypt(self, ciphertext_bytes, key=None):
        if key is None:
            key = self._private_key
        return key.decrypt(ciphertext_bytes)
