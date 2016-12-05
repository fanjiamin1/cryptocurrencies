
def modularpoweroftwo(number,poweroftwo,module):
    #returns number**(2**poweroftwo) % module
    value=number%module
    currexponent=0
    while currexponent<poweroftwo:
        value=(value*value)%module
        currexponent+=1
        
    return value


        
def fastmodularexponentiation(number,exponent,module):
    value=1
    for i in range(len(bin(exponent)[2:][::-1])):
        if bin(exponent)[2:][::-1][i]=='1':
            value*=modularpoweroftwo(number,i,module)
    return value

print(fastmodularexponentiation(5,3,200))
        
    
    
