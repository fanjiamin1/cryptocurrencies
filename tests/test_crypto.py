from pychat.crypto import Naive, Vigenere, AES


message = "Hello, world!"


def test_naive_encrypt_decrypt():
    key = 89
    cipher = Naive(key)
    assert cipher.decrypt(cipher.encrypt(message)) == message

def test_vigenere_encrypt_decrypt():
    key = "sixteen char key"
    cipher = Vigenere(key)
    assert cipher.decrypt(cipher.encrypt(message)) == message

def test_aes_encrypt_decrypt():
    key = "sixteen char key"
    message = "Attack FLAT n3rd"
    cipher = AES(key)
    assert cipher.decrypt(cipher.encrypt(message)) == message

def test_aes_encrypt_decrypt():
    key = "Non sixteen character key"
    message = "A hopefully non sixteen character message"
    cipher = AES(key)
    assert cipher.decrypt(cipher.encrypt(message)) == message
