from abc import ABCMeta, abstractmethod


class Cipher(metaclass=ABCMeta):
    @abstractmethod
    def encrypt(self, cleartext):
        pass

    @abstractmethod
    def decrypt(self, ciphertext):
        pass
