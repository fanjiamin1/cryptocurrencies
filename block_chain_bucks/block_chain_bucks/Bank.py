import os
import sys
import socket
from .crypto import RSA
from block_chain_bucks import Block, BlockChain
from Crypto.Hash.SHA256 import SHA256Hash as SHA256


BUFSIZE = 2**12
ENCODING = "utf-8"


class Bank:
    def __init__(
                  self
                , port=9001
                , keys=None
                , identity=None  # TODO
                ):
        # Initialize socket
        self.socket = socket.socket(
                                     socket.AF_INET
                                   , socket.SOCK_DGRAM
                                   )
        self.socket.bind(("", port))
        # Initialize key dictionary and identity
        self.keys = keys
        self.identity = identity
        # Initialize block chain
        genesis_payload = "".join((
                                    "pay "
                                  , self.identity
                                  , " 0 "
                                  , self.identity
                                  , " 1000"
                                  ))
        genesis_block = Block(
                               SHA256(self.identity.encode()).digest()
                             , genesis_payload
                             )
        self.block_chain = BlockChain(genesis_block)

    def find_balance(self,id):
        for block in reversed(self.blockchain):
            transaction_words=block.payload.decode(Block.ENCODING).split(' ')
            out_id_index=-1
            if id in transaction:
                #pythonic way of finding output part of the id
                out_id_index=transaction_words[:transaction_words.index(id)+1].index(id)+transaction_words.index(id)+1
                out_amount_index = out_id_index+1
                break
            if out_id_index==-1:
                #TODO:need to account for founder transaction
                #otherwise no balance can ever exist
                return 0
        try:
            return int(transaction_words[out_amount_index])
        except:
            #this means we have a malformed transaction in the block-chain
            system.exit("blockchain contained invalid transfer or balance checking is bugged")

    def start(self):
        try:
            while True:
                print("--------------------------------"*2)
                print("BLOCKCHAIN STATUS:")
                for block in self.block_chain:
                    print("\t", str(block.payload)[:64], "...")
                print("--------------------------------"*2)
                data, address = self.socket.recvfrom(BUFSIZE)
                if data:
                    try:
                        message = data.decode()
                        message_words = message.split(' ')
                        command = message_words[0].lower()

                        if command == "pay":
                            self.pay(message_words, address)
                        elif command == "query":
                            self.query(message_words, address)
                        else:
                            self.invalid(message_words, address)
                    except Exception as e:
                        print("EXCEPTION:", e)
        except KeyboardInterrupt:
            print()
            print("Closing bank for now")

    def check_pay_command(self,message_words):
        #checks whether or not transaction can be added to blockchain
        inids=message_words[1:message_words[2:].index(message_words[1])+2:2]
        outids=message_words[message_words[2:].index(message_words[1])+2::2][:len(inids)]
        try:
            inamounts=[int(x) for x in message_words[3:message_words[2:].index(message_words[1])+2:2]]
            outamounts=[int(x) for x in message_words[message_words[2:].index(message_words[1])+3::2]][:len(inids)]
        except:
            #not all amounts were ints
            return False
        if not sum(inamounts)==sum(outamounts):
            #transactions did not add up
            return False
        if not inids==outids:
            #ids malformed
            return False
        #command is well-formed at this point
        #the below multiline comment will verify that account balances allow
        #the operation
        """
        for i in range(len(inamounts)):
            if self.blockchain.balance(inids[i])<inamounts[i]:
                return False
        """

        return True




    def pay(self, message_words, address):
        print("Payment request processing...")
        #As I currently understand it, commands should still take the form
        #pay person1 (amount person 1 wants to spend) person 2 (amount person 2 wants to spend) ...
        #while blockchain transactions should have person1 (balance of person 1 before transaction) ...
        #this will force a reformat before submitting to blockchain
        #TODO: reformat transaction and put into blockchain
        #TODO: These awful slices are super useful, should be refactored into
        #seperate function instead of being copied around code
        #the below multiline comment contains code that will reformat transactions
        #and submit them to the blockchain
        inids=message_words[1:message_words[2:].index(message_words[1])+2:2]
        outids=message_words[message_words[2:].index(message_words[1])+2::2]
        inamounts=[int(x) for x in message_words[3:message_words[2:].find(message_words[1])+2:2]]
        outamounts=[int(x) for x in message_words[message_words[2:].index(message_words[1])+3::2]]

        #reformats so inamounts[i] is starting balance and outamounts[i] is ending balance
        for i in range(len(inids)):
            balance=self.blockchain.balance(inids[i])
            outamounts[i]=balance-inamounts[i]+outamounts[i]
            inamounts[i]=balance
        #reassemble final string
        blockchainstring=""
        for i in range(len(inids)):
            blockchainstring+=" " + inids[i]
            blockchainstring+=" " + str(inamounts[i]) 
        for i in range(len(inids)):
            blockchainstring+=" " + outids[i]
            blockchainstring+=" " + str(outamounts[i]) 
        self.blockchain.append(blockchainstring)

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


def _get_identity_from_key_file(file_name):
    return SHA256(RSA.key_from_file(file_name).exportKey()).hexdigest()


if __name__ == "__main__":
    module_directory = os.path.split(os.path.dirname(__file__))[0]
    root_directory = os.path.split(module_directory)[0]
    key_directory = os.path.join(root_directory, "keys")

    # Construct absolute paths to key files
    bank_public_key_file = os.path.join(key_directory, "bank_public.rsk")
    hugo_public_key_file = os.path.join(key_directory, "hugo_public.rsk")
    ivar_public_key_file = os.path.join(key_directory, "ivar_public.rsk")
    ragnar_public_key_file = os.path.join(key_directory, "ragnar_public.rsk")

    # Load keys
    bank_public_key = RSA.key_from_file(bank_public_key_file)
    hugo_public_key = RSA.key_from_file(hugo_public_key_file)
    ivar_public_key = RSA.key_from_file(ivar_public_key_file)
    ragnar_public_key = RSA.key_from_file(ragnar_public_key_file)

    # Construct identities from keys
    bank_identity = SHA256(bank_public_key.exportKey()).hexdigest()
    hugo_identity = SHA256(hugo_public_key.exportKey()).hexdigest()
    ivar_identity = SHA256(ivar_public_key.exportKey()).hexdigest()
    ragnar_identity = SHA256(ragnar_public_key.exportKey()).hexdigest()

    keys = {
             bank_identity: bank_public_key
           , hugo_identity: hugo_public_key
           , ivar_identity: ivar_public_key
           , ragnar_identity: ragnar_public_key
           }

    print(keys)

    bank = Bank(keys=keys, identity=bank_identity)
    bank.start()
