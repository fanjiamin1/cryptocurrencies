import os
import socket
from .crypto import RSA
from itertools import chain
from Crypto.Hash.SHA256 import SHA256Hash as SHA256


class BankConnection:
    def __init__(self, ip="127.0.0.1", port=9001):
        self.rsa = RSA()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.address = (ip, port)

    def pay(self, *identity_amount_pairs):
        preamble = ["pay"]
        before = []
        after = []
        signatures = []  # TODO: Eventually do signatures
        for identity, amount in identity_amount_pairs:
            before.append(identity)
            after.append(identity)
            if amount == 0:
                before.append("0")
                after.append("0")
            elif amount > 0:
                before.append("0")
                after.append(str(amount))
            else:
                before.append(str(abs(amount)))
                after.append("0")
        message = " ".join(chain(preamble, before, after, signatures))
        print("Sent:", message)
        message = message.encode()
        self.socket.sendto(message, self.address)

def _get_identity_from_key_file(file_name):
    return SHA256(RSA.key_from_file(file_name).exportKey()).hexdigest()

if __name__ == "__main__":
    module_directory = os.path.split(os.path.dirname(__file__))[0]
    root_directory = os.path.split(module_directory)[0]
    key_directory = os.path.join(root_directory, "keys")

    hugo_public_key_file = os.path.join(key_directory, "hugo_public.rsk")
    ivar_public_key_file = os.path.join(key_directory, "ivar_public.rsk")
    ragnar_public_key_file = os.path.join(key_directory, "ragnar_public.rsk")


    hugo_identity = _get_identity_from_key_file(hugo_public_key_file)
    ivar_identity = _get_identity_from_key_file(ivar_public_key_file)
    ragnar_identity = _get_identity_from_key_file(ragnar_public_key_file)

    bank_connection = BankConnection()
    for _ in range(5):
        bank_connection.pay((ragnar_identity, 2), (ivar_identity, -1), (hugo_identity, -1))
