import threading
from Crypto.Hash import SHA256 as SHA

class StoppableHashThread(threading.Thread):
"""
    takes in a block and a target, hashes
    until it finds a hash under that target
    or receives a stop() command
"""
    def __init__(self,block_contents,target):
        #accepts blocks in the form of a list of strings
        #each of which is a field of the previous block
        super(StoppableThread,self).__init__()
        self.stopped=False
        self.prehash=SHA()

        self.nonce=0
        for item in block_contents:
            self.prehash.update(str.encode(item))

        self.found=False

    def stop(self):
        self.stopped=True

    def myhash(self):
        #steal this from proofofwork
        temphash=self.prehash.copy()
        temphash.update(str.encode(str(self.nonce))) 
        self.nonce+=1 
        return temphash.digest()


    def run(self):
        while not stopped:
            guess=hash()
            if myHash[0:len(target)] == target:
                self.found=True
                return
                








