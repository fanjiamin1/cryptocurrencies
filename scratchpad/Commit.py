import random
import Coin
from Crypto.Hash import SHA256


def nonce():
	return random.getrandbits(128)

def commit(m, r):
	return ( SHA256.new(str.encode(str(m)) + str.encode(str(r))).hexdigest() )

m = Coin.flip_coin()
r = nonce()
c = commit(m, r)