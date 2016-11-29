import abc


class Cipher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def salt(size):
        pass

    @abc.abstractmethod
    def myEncrypt(self, cleartext):
        pass

    @abc.abstractmethod
    def myDecrypt(self, ciphertext):
        pass
