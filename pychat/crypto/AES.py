import Crypto.Cipher
from Crypto import Random
from pychat.misc.encoding_tools import ENCODING


SALT_LENGTH = 4
BLOCK_SIZE = Crypto.Cipher.AES.block_size
MESSAGE_SLICE_SIZE = BLOCK_SIZE - SALT_LENGTH
PADDING_CHARACTER = '`'


class AES:
    def __init__(self, key):
        self.key = bytes(key, ENCODING)
        self.cipher = Crypto.Cipher.AES.new(
                                             self.key
                                           , Crypto.Cipher.AES.MODE_ECB
                                           )

    def get_salt(self):
        return Random.new().read(SALT_LENGTH)

    def encrypt(self, message):
        ciphertexts = []
        index = 0
        while index < len(message):
            message_slice = message[index:index+MESSAGE_SLICE_SIZE]
            missing = MESSAGE_SLICE_SIZE - len(message_slice)
            if missing != 0:
                message_slice += PADDING_CHARACTER*missing
            message_slice = bytes(message_slice, ENCODING)
            salted_message_slice = message_slice + self.get_salt()
            ciphertext = self.cipher.encrypt(salted_message_slice)
            ciphertexts.append(ciphertext)
            index += MESSAGE_SLICE_SIZE
        return b"".join(ciphertexts)
 
    def decrypt(self, message):
        cleartexts = []
        index = 0
        while index < len(message):
            message_slice = message[index:index+BLOCK_SIZE]
            salted_cleartext = self.cipher.decrypt(message_slice)
            cleartext = salted_cleartext[:-SALT_LENGTH].decode(ENCODING)
            cleartexts.append(cleartext)
            index += BLOCK_SIZE
        cleartexts[-1] = cleartexts[-1].rstrip(PADDING_CHARACTER)
        return "".join(cleartexts)
