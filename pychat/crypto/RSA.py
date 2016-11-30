from Crypto.PublicKey import RSA

newkey=RSA.generate(1024)

message=b"hello world!"

print(newkey.encrypt(message,b"I'm not sure why this argument isn't optional"))

print(newkey.decrypt(newkey.encrypt(message,b'this feels silly')))

destination=open('key.txt','w')

destination.write(str(newkey.exportKey("PEM")))
