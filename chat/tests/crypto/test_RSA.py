from chat.crypto import RSA
from chat.misc.encoding_tools import ENCODING


def test_rsa_encrypt_decrypt_1():
    key = RSA.generate_key()
    cipher = RSA(key)
    message = bytes("Hello, world! I'm @ the c3||7re?", ENCODING)
    assert cipher.decrypt(cipher.encrypt(message)) == message

def test_rsa_encrypt_decrypt_2():
    key = RSA.generate_key()
    message = bytes("A hopefully non sixteen character message", ENCODING)
    cipher = RSA(key)
    assert cipher.decrypt(cipher.encrypt(message)) == message
