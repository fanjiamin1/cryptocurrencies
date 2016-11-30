from pychat.crypto import RSA
import gnupg 


gpg=gnupg.GPG()
with open("RUkey.asc",'r') as keyfile:
    key=""
    for line in keyfile:
        key+=keyfile.readline()
        #key+='\n'
    print(key)
    gpg.encrypt("Hi there, Jonathan",key)
    #cipher=RSA(key)


