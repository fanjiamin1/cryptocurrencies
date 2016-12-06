#TODO: format id to 32 bytes, done for perform_transaction
#TODO: encrypt everything, possibly require encrypted+signed payments
# This will require a seperate key management, possibly an extra DB, with
# each agent having access to a master store of all public keys, as well
# as their own, built-in, private keys
#need to add session tracking, with reinitialisation on each session
#could probably be hacked out of db finding highest session number

#server now encrypts 



import socket
import uuid
from query import transaction
from crypto import RSA


class server:
    

    def __init__(self,port=9001):
        #needs to load the db

        self.socket=socket.socket(socket.AF_INET
                                 ,socket.DGRAM)
        socket.bind('',port)
        self.rsa=RSA()
        self.publickey, self.privatekey=self.rsa.generate_key_pair(2)
        #post public key to public file, after that, self.publickey
        #should contain public key of the party that is being
        #addressed, so that we can encrypt using it


    def generate_transaction_id():
        #generates a string that is unique for this session at least
        #probabilistically, this shouldn't collide, but it would bear
        #checking to be perfect
        #this actually means we only have a 16 bytes of effective namespace
        #but searching it is as hard as a 32 byte namespace, it's plenty big
        #and plenty hard to search
        #this will probably be deprecated for sql generated id's, which should
        #be secure enough once we encrypt
        return uuid.uuid4().bytes+uuid.uuid4().bytes

    def perform_transaction(message_words):
        if len(message_words)!=3:
            return 'False'
        payer=message_words[1]
        receiver=message_words[2]
        amountstring=message_words[3]
        try:
            amount=(int) amountstring
        except:
            return 'False'
        #TODO:confirm that payer and receiver are valid
        #and that payer can afford the payment
        #needs db interface
        #db interface now promises this functionality
        transaction_id=transaction(payer,receiver,words)
        if not transaction_id is None:
            #formatting transaction id to be 32 bytes
            string_id=str(transaction_id)
            if len(string_id)>32:
                system.exit("we ran out of transaction ID's, that's a lot"
                           +"of transactions")
            else:
                string_id=string_id.ljust(32,'0')

    
            return transaction_id
        else:
            return 'False'

    def verify_transaction(message_words):
        if len(message_words)!=4:
            return 'False'
        payer=message_words[1]
        receiver=message_words[2]
        transaction_id=message_words[3]
        amountstring=message_words[4]
        try:
            amount=(int) amountstring
        except:
            return 'False'
        transaction_confirmed=True
        #TODO:confirm that payer and receiver are valid
        #and that payer can afford the payment
        #needs db interface, if any tests fail, set transaction_confirmed
        #to False
        #will be delivered by db
        return transaction_confirmed


    def start():
        while True:
            #TODO:use addr to set public key so we can 
            #encrypt data specifically for the user being addressed
            data, addr = self.socket.recvfrom(1024)
            if data:
                #parse data
                #TODO:verify message words function
                message_words=data.partition(' ')
                #TODO:encrypt this on the way out

                if message_words[0].lower()=='pay':
                    message=self.perform_transaction(message_words)
                    self.socket.sendto(self.rsa.encrypt(message)
                                      ,addr)
                elif message_words[0].lower()=='query':
                    message=self.verify_transaction(message_words)
                    self.socket.sendto(self.rsa.encrypt(message)
                                      ,addr)
                else:
                    #encrypt answer to failed commands? maybe not
                    self.socket.sendto('unknown command, try again', addr)

