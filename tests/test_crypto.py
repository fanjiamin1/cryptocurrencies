import pychat.crypto.naive as naive


def test_naive_encrypt_decrypt():
    key = 89
    assert naive.decrypt(key, naive.encrypt(key, "Hello, world")) == "Hello, world"
