from Crypto.Cipher import AES
from Crypto import Random

key=b'sixteen byte key'

iv= Random.new().read(AES.block_size)
#If the below is run, the gibberish that follows the message is zeroes
#iv= b'0000000000000000'
cipher=AES.new(key,AES.MODE_ECB, iv)

message="attack flat dawn"
noiv=cipher.encrypt('attack flat dawn')
withiv=cipher.encrypt(iv+ b'attack flat dawn')
#print(cipher.decrypt(cipher.encrypt(iv +b"attack flat dawn")))

dec_iv= Random.new().read(AES.block_size)
decryptor= AES.new(key,AES.MODE_ECB,dec_iv)

#print('without iv decryptor found: '+ str(decryptor.decrypt(noiv)))
#print('with iv decryptor found: '+ str(decryptor.decrypt(withiv)) )

def keygen():
    #add key randomisation or or keys as input here
    key=b'sixteen byte key'
    #quite a bit of testing found no significance to the value of iv
    iv= Random.new().read(AES.block_size)
    cipher=AES.new(key,AES.MODE_ECB, iv)

def salt(size):
    salt = Random.new().read(size)
    return salt

def myEncrypt(message,key):
    iv= Random.new().read(AES.block_size)
    saltsize = 16 - len(message)
    cipher=AES.new(key,AES.MODE_ECB, iv)
    
    #Padding
    pad = ' ' * saltsize ;
    pad_message = message + pad
    
    #Encrypt + Salting
    ciphertext = cipher.encrypt(pad_message)
    ciphertext_salted = salt(saltsize) + ciphertext
   
    return ciphertext_salted
    
def myDecrypt(message,key):
    iv= Random.new().read(AES.block_size)
    cipher=AES.new(key,AES.MODE_ECB, iv)
    
    #Decrypt
    pad_text = cipher.decrypt(message)
    
    #De-padd
    saltsize = 16 - len(message)
    cleartext = pad_text[-saltsize:]
    return cleartext

print( myDecrypt( myEncrypt('anthropocentrism', b'sixteen byte key') , b'sixteen byte key' ) )
