from broadchat.crypto import RSA


def test_rsa_encrypt_decrypt_1():
    key = RSA.generate_key()
    cipher = RSA(key)
    message = "Hello, world! I'm @ the c3||7re?"
    assert cipher.decrypt(cipher.encrypt(message)) == message

def test_rsa_encrypt_decrypt_2():
    key = "Non sixteen character key"
    message = "A hopefully non sixteen character message"
    cipher = RSA(key)
    assert cipher.decrypt(cipher.encrypt(message)) == message
