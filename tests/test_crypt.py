from pychat import encrypt, decrypt

def test_encrypt_decrypt():
    key = 89
    assert decrypt(key, encrypt(key, "Hello, world")) == "Hello, world"
