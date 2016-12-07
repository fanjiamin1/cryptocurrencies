import socket
from .crypto import RSA


BUFSIZE = 2**12
ENCODING = "utf-8"


class Bank:
    def __init__(self, port=9001, public_key_file=None, private_key_file=None):
        self.socket = socket.socket(
                                     socket.AF_INET
                                   , socket.SOCK_DGRAM
                                   )
        self.socket.bind(("", port))
        self.rsa = RSA()
        if public_key_file is not None:
            self.rsa.set_public_key(RSA.key_from_file(public_key_file))
        if private_key_file is not None:
            self.rsa.set_private_key(RSA.key_from_file(private_key_file))

    def start(self):
        while True:
            data, address = self.socket.recvfrom(BUFSIZE)
            if data:
                try:
                    message = self.rsa.decrypt(data)
                    message = message.decode()
                    message_words = message.split(' ')
                    command = message_words[0].lower()

                    self.rsa.set_public_key(query.get_key(message_words[1]))
                    signature = message_words[-1]
                    verifiable_message = "".join(message_words[:-1])
                    signature = int(signature)
                    assert self.rsa.verify(verifiable_message, signature)

                    if command == "pay":
                        self.pay(message_words, address)
                    elif command == "query":
                        self.query(message_words, address)
                    else:
                        self.invalid(message_words, address)
                except Exception as e:
                    print("EXCEPTION:", e)

    def pay(self, message_words, address):
        reply = b"A reply"
        print(reply)
        #encrypted_reply = self.rsa.encrypt(reply)
        #self.socket.sendto(
        #                    encrypted_reply
        #                  , address
        #                  )
        self.socket.sendto(b"Pay request", address)

    def query(self, message_words, address):
        reply = b"A reply"
        print(reply)
        #encrypted_reply = self.rsa.encrypt(reply)
        #self.socket.sendto(
        #                    encrypted_reply
        #                  , address
        #                  )
        self.socket.sendto(b"Query request", address)

    def invalid(self, message_words, address):
        self.socket.sendto(b"Invalid request", address)


if __name__ == "__main__":
    key_directory = os.path.join(os.path.split(os.path.dirname(__file__))[0], "keys")
    public_key_file = os.path.join(key_directory, "bank_public.rsk")
    private_key_file = os.path.join(key_directory, "bank_private.rsk")
    bank = Bank(public_key_file=public_key_file, private_key_file=private_key_file)
    bank.start()
