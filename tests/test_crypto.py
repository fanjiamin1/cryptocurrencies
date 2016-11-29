from pychat import Naive


def test_naive_encrypt_decrypt():
    key = 89
    cipher = Naive(key)
    assert cipher.decrypt(cipher.encrypt("Hello world")) == "Hello world"
