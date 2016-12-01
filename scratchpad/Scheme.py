import Coin
import Commit

#Bob picks
a = Coin.flip_coin()

#Alice flips
b = Coin.flip_coin()

#Bob runs the commit algorithm and give alice the public commitment
r_bob = Commit.nonce()
c_bob = Commit.commit(a, r_bob)

#Alice does too
r_alice = Commit.nonce()
c_alice = Commit.commit(b, r_alice)

#Both runs the reveal
if (c_bob != Commit.commit(a, r_bob)):
	print("Bob lied!")
elif (c_alice != Commit.commit(b, r_alice)):
	print("Alice lied!")
else:
	shared_coin = a ^ b
	if (shared_coin == 1):
		print("Bob wins")
	else:
		print("Alice wins")