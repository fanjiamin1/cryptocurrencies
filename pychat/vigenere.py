
debug=False

key="cryptocurrencyclasscanbedifficultbutisprobablyrewardingonlytimewilltellthough"

alphabet="abcdefghijklmnopqrstuvwxyz"

def keygen():
    pass
def encrypt(message, key):
    output=''
    for i in range(len(message)):
        if debug: print('checking on: '+message[i])
        shift=alphabet.index(key[i%len(key)])
        output+=alphabet[(alphabet.index(message[i])+shift)%len(alphabet)]
    return output

def decrypt(message,key):
    output=''
    for i in range(len(message)):
        if debug: print('checking on: '+message[i])
        shift=alphabet.index(key[i%len(key)])
        output+=alphabet[(alphabet.index(message[i])-shift)%len(alphabet)]
    return output
 
print('testing')
message='helloworld'
print('message: '+ message)
print(encrypt(message,key))
print(decrypt(encrypt(message,key),key))
