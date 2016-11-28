from pychat import encrypt, decrypt

def test_encrypt_decrypt():
    assert decrypt(encrypt("Hello, world")) == "Hello, world"
