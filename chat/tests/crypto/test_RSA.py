from chat.crypto import RSA
from chat.misc.encoding_tools import ENCODING


def test_rsa_encrypt_decrypt_1():
    public, private = RSA.generate_key_pair()
    cipher = RSA()
    message = bytes("Hello, world! I'm @ the c3||7re?", ENCODING)
    assert cipher.decrypt(cipher.encrypt(message, public), private) == message

def test_rsa_encrypt_decrypt_2():
    public, private = RSA.generate_key_pair()
    message = bytes("A hopefully non sixteen character message", ENCODING)
    cipher = RSA()
    cipher.set_public_key(public)
    cipher.set_private_key(private)
    assert cipher.decrypt(cipher.encrypt(message)) == message
