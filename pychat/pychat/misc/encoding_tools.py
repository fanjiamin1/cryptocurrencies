ENCODING = "utf-8"
MAX_BYTE = 256


def char2byte(character):
    return ord(character) % MAX_BYTE


def byte2char(byte):
    return chr(byte)
