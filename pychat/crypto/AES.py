import Crypto.Cipher
from Crypto import Random
from pychat.misc.encoding_tools import ENCODING
from pychat.crypto import Cipher


SALT_SIZE = 2
BLOCK_SIZE = Crypto.Cipher.AES.block_size
MESSAGE_SLICE_SIZE = BLOCK_SIZE - SALT_SIZE
PADDING_CHARACTER = '\x80'


class AES(Cipher):
    def __init__(self, key):
        self._key = bytes(key, ENCODING)
        self._cipher = Crypto.Cipher.AES.new(self._key, BLOCK_SIZE)
        self._random = Random.new()

    def _get_salt(self):
        return self._random.read(SALT_SIZE)

    def encrypt(self, message):
        # Encode salted slices of the message before returning the joined result
        ciphertexts = []
        index = 0
        while index < len(message):
            message_slice = message[index:index+MESSAGE_SLICE_SIZE]
            missing = MESSAGE_SLICE_SIZE - len(message_slice)
            if missing != 0:
                message_slice += PADDING_CHARACTER*missing
            message_slice = bytes(message_slice, ENCODING)
            salted_message_slice = message_slice + self._get_salt()
            ciphertext = self._cipher.encrypt(salted_message_slice)
            ciphertexts.append(ciphertext)
            index += MESSAGE_SLICE_SIZE
        return b"".join(ciphertexts)

    def decrypt(self, message):
        cleartexts = []
        index = 0
        while index < len(message):
            message_slice = message[index:index+BLOCK_SIZE]
            salted_cleartext = self._cipher.decrypt(message_slice)
            cleartext = salted_cleartext[:-SALT_SIZE].decode(ENCODING)
            cleartexts.append(cleartext)
            index += BLOCK_SIZE
        cleartexts[-1] = cleartexts[-1].rstrip(PADDING_CHARACTER)
        return "".join(cleartexts)
