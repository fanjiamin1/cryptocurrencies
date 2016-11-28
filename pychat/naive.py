def encrypt(message):
    return bytes(message, "utf-8")

def decrypt(ciphertext):
    return ciphertext.decode("utf-8")
