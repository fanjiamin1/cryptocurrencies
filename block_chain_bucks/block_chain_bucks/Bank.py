import socket
from .crypto import RSA
from block_chain_bucks import Block
from Crypto.Hash.SHA256 import SHA256Hash as SHA256


BUFSIZE = 2**12
ENCODING = "utf-8"


class Bank:
    def __init__(self, port=9001, public_key_file=None, private_key_file=None):
        self.socket = socket.socket(
                                     socket.AF_INET
                                   , socket.SOCK_DGRAM
                                   )
        self.socket.bind(("", port))
        pubkey=RSA.key_from_file(public_key_file)
        self.rsa = RSA()
        sha = SHA256()
        sha.update(self.pubkey)
        self.identity=sha.hexdigest()
        genesis_block=Block( identity, identity+b" 0"+ identity+b" 1000000")
        self.blockchain=BlockChain(genesis_block)
        if public_key_file is not None:
            self.rsa.set_public_key(pubkey)
        if private_key_file is not None:
            self.rsa.set_private_key(RSA.key_from_file(private_key_file))

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
        reply = b"A reply"
        print(reply)
        #TODO: check_pay_command(message_words) and fail if it is false
        #encrypted_reply = self.rsa.encrypt(reply)
        #self.socket.sendto(
        #                    encrypted_reply
        #                  , address
        #                  )
        #As I currently understand it, commands should still take the form
        #pay person1 (amount person 1 wants to spend) person 2 (amount person 2 wants to spend) ...
        #while blockchain transactions should have person1 (balance of person 1 before transaction) ...
        #this will force a reformat before submitting to blockchain
        #TODO: reformat transaction and put into blockchain
        #TODO: These awful slices are super useful, should be refactored into
        #seperate function instead of being copied around code
        #the below multiline comment contains code that will reformat transactions
        #and submit them to the blockchain
        """
        inids=message_words[1:message_words[2:].index(message_words[1])+2:2]
        outids=message_words[message_words[2:].index(message_words[1])+2::2]
        try:
            inamounts=[int(x) for x in message_words[3:message_words[2:].find(message_words[1])+2:2]]
            outamounts=[int(x) for x in message_words[message_words[2:].index(message_words[1])+3::2]]
        except:
            #never happens, same slicing is done in check pay command
            System.exit("ungraceful failure in pay, amounts werent ints")
            
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
        """

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
