ENCODING = "utf-8"

def encrypt(key, cleartext):
    ciphertext = bytes(byte^key for byte in bytes(cleartext, ENCODING))
    return ciphertext

def decrypt(key, ciphertext):
	cleartext = bytes(byte^key for byte in ciphertext).decode(ENCODING)
	return cleartext
