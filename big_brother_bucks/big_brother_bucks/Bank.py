#TODO: format id to 32 bytes, done for perform_transaction
#TODO: encrypt everything, possibly require encrypted+signed payments
# This will require a seperate key management, possibly an extra DB, with
# each agent having access to a master store of all public keys, as well
# as their own, built-in, private keys
#need to add session tracking, with reinitialisation on each session
#could probably be hacked out of db finding highest session number


import socket
import uuid
#import .query as query
from .crypto import RSA
import os


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

    def perform_transaction(self, message_words):
        if len(message_words) != 4:
            return repr(False)
        payer = message_words[1]
        receiver = message_words[2]
        amountstring = message_words[3]
        try:
            amount = int(amountstring)
        except:
            return repr(False)
        #TODO:confirm that payer and receiver are valid
        #and that payer can afford the payment
        #needs db interface
        #db interface now promises this functionality
        transaction_id = query.transaction(payer, receiver, words)
        if transaction_id is not None:
            #formatting transaction id to be 32 bytes
            string_id = str(transaction_id)
            if len(string_id) > 32:
                system.exit("Transaction limit exceeded")
            else:
                string_id = string_id.ljust(32, '0')
            return transaction_id
        else:
            return repr(False)

    def verify_transaction(self, message_words):
        if len(message_words) != 5:
            return repr(False)
        payer = message_words[1]
        receiver = message_words[2]
        transaction_id = message_words[3]
        amountstring = message_words[4]
        try:
            amount = int(amountstring)
        except:
            return repr(False)
        tpayer, treceiver, tamount, tsession = query.look_up_transaction(transaction_id)
        return repr(payer == tpayer and receiver == treceiver and amount == tamount)


    def start(self):
        while True:
            data, address = self.socket.recvfrom(BUFSIZE)
            if data:
                try:
                    message = self.rsa.decrypt(data)
                    message = message.decode()
                    message_words = message.split(' ')
                    command = message_words[0].lower()

                    # TODO: Fetch the public key and use it to verify the message
                    #self.rsa.verify(message)

                    if command == "pay":
                        self.pay(message_words, address)
                    elif command == "query":
                        self.query(message_words, address)
                    else:
                        self.invalid(message_words, address)
                except Exception as e:
                    print("EXCEPTION:", e)

    def pay(self, message_words, address):
        #self.rsa.set_public_key(query.get_key(message_words[1]))
        reply = self.perform_transaction(message_words)
        print(reply)
        reply = bytes(reply, ENCODING)
        #encrypted_reply = self.rsa.encrypt(reply)
        #self.socket.sendto(
        #                    encrypted_reply
        #                  , address
        #                  )

    def query(self, message_words, address):
        #self.rsa.set_public_key(query.get_key(message_words[2]))
        reply = self.verify_transaction(message_words)
        print(reply)
        reply = bytes(reply, ENCODING)
        #encrypted_reply = self.rsa.encrypt(reply)
        #self.socket.sendto(
        #                    encrypted_reply
        #                  , address
        #                  )

    def invalid(self, message_words, address):
        self.socket.sendto(b"Invalid request", address)


if __name__ == "__main__":
    key_directory = os.path.join(os.path.split(os.path.dirname(__file__))[0], "keys")
    public_key_file = os.path.join(key_directory, "bank_public.rsk")
    private_key_file = os.path.join(key_directory, "bank_private.rsk")
    bank = Bank(public_key_file=public_key_file, private_key_file=private_key_file)
    bank.start()
