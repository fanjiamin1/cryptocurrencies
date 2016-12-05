import socket
import uuid


class server:
    

    def __init__(self,port=9001):
        #needs to load the db and set nextid appropriately

        self.socket=socket.socket(socket.AF_INET
                                 ,socket.DGRAM)
        socket.bind('',port)

    def generate_transaction_id():
        #generates a string that is unique for this session at least
        #probabilistically, this shouldn't collide, but it would bear
        #checking to be perfect
        #this actually means we only have a 16 bytes of effective namespace
        #but searching it is as hard as a 32 byte namespace, it's plenty big
        #and plenty hard to search
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
        #needs db interface, if any tests fail, set transaction_success
        #to False
        transaction_success=True
        if transaction_success:
            #TODO:Generate transaction ID , file transaction in db
            transaction_id=generate_transaction_id()
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
        return transaction_confirmed


    def start():
        while True:
            data, addr = self.socket.recvfrom(1024)
            if data:
                #parse data
                #TODO:verify message words function
                message_words=data.partition(' ')
                if message_words[0].lower()=='pay':
                    self.socket.sendto(self.perform_transaction(message_words)                                      ,addr)
                elif message_words[0].lower()=='query':
                    self.socket.sendto(self.verify_transaction(message_words)
                                      ,addr)
                else:
                    self.socket.sendto('unknown command, try again', addr)

