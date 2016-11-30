import time
from Crypto.Hash import SHA256
from bitstring import BitArray

goal = 0
nonce = 0
target = '0' * 3
message = "Hello World !"

timestamp = str(time.time()) 

start = time.time()
while goal == 0:
	nonce += 1
	myHash = ( SHA256.new(str.encode( message + str(nonce) ) ) ).hexdigest()
	if myHash[0:len(target)] == target:
 		goal = 1
end = time.time()

print(myHash)
print(end - start)
print(nonce)
