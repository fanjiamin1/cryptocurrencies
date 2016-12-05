from chat.crypto import RSA
from chat.misc.encoding_tools import ENCODING


def test_rsa_encrypt_decrypt_1():
    private, public = RSA.generate_key_pair()
    cipher = RSA()
    message = bytes("Hello, world! I'm @ the c3||7re?", ENCODING)
    assert cipher.decrypt(cipher.encrypt(message, public), private) == message

def test_rsa_encrypt_decrypt_2():
    private, public = RSA.generate_key_pair()
    message = bytes("A hopefully non sixteen character message", ENCODING)
    cipher = RSA()
    cipher.set_private_key(private)
    cipher.set_public_key(public)
    assert cipher.decrypt(cipher.encrypt(message)) == message
