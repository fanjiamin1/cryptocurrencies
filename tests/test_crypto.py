from pychat import Naive, Vigenere


message = "Hello, world!"


def test_naive_encrypt_decrypt():
    key = 89
    cipher = Naive(key)
    assert cipher.decrypt(cipher.encrypt(message)) == message

def test_vigenere_encrypt_decrypt():
    key = "sixteen char key"
    cipher = Vigenere(key)
    assert cipher.decrypt(cipher.encrypt(message)) == message
