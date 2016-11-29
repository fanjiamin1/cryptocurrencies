import abc


class Cipher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def encrypt(self, cleartext):
        pass

    @abc.abstractmethod
    def decrypt(self, ciphertext):
        pass
