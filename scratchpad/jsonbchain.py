import hashlib
import json


class Block(list):
    def __new__(cls, hash_pointer, content):
        return list.__new__(cls, (hash_pointer, content))


class BlockChain(list):
    def __init__(self, genesis_block):
        self.chain = [genesis_block]
    def dump(self, file_name):
        with open(file_name, "w") as dump_file:
            json.dump(self.chain, dump_file)
    def load(self, file_name):
        with open(file_name, "r") as dump_file:
            self.chain = json.load(dump_file)
