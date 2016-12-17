from random import randint,choice
from functools import reduce

#TODO: 

TOP_PRIME_PER_BYTE=251

#takes in k,n for (k,n) threshold scheme to contain a secret string S
#returns a list of shares, each share is a list of len(S) 2-tuples, each
#of which is a share in one of the letters of the string S
#also outputs the prime used in modular calculations, which is 251
def get_byte_shares(k,n,S):
    #the highest prime that can be contained in one byte
    topprime=TOP_PRIME_PER_BYTE
    
    charactershares=[]
    for character in S:
        secret_number=ord(character)
        print('character was:',character)
        print('secret number was:',secret_number)
        if secret_number>TOP_PRIME_PER_BYTE:
            raise ValueError('Character:',character,'is not supported, it has an order over 251')
        #want to create a polynomial of degree k-1 so we need k constants
        #we dissallow coefficients of 0 for simplicity, we must avoid zero in
        #the highest order coefficient
        coefficients=[secret_number]
        coefficients.extend(randint(1,topprime-1) for _ in range(k-1))
        #confirm that the secret is indeed contained as the
        #constant in the resulting polynomial
        assert secret_number==evaluate_polynomial(0,coefficients)%topprime

        used_xvals=[]
        found_yvals=[]

        for i in range(n):
            xval=randint(1,topprime-1)
            while xval in used_xvals:
                #theoretically can be infinite, maybe do something about that,
                #call needs to be malfromed for that to happen though
                xval=randint(1,topprime-1)
            used_xvals.append(xval)
            found_yvals.append(evaluate_polynomial(xval,coefficients)%topprime)
        #add the shares
        print('charactershares length before append:',len(charactershares))
        charactershares.append([(used_xvals[i],found_yvals[i]) for i in range(n)])
        print('charactershares length after append:',len(charactershares))
    #charactershares now contains len(S) lists of n shares each
    #each share is now a list of tuples, one for each letter of the secret message
    
    shares=[ list(map(lambda x:x[i],charactershares)) for i in range(n)]
    
    

    #shares has n lists, each containing len(S) tuples, which are one users keys for each byte
    return topprime,shares

#takes in shares in the same format as get_shares outputs
#outputs the secret string
def combine_byte_shares(k,n,p,shares):
    charactershares= [ [shares[k][i] for k in range(len(shares))] for i in range(len(shares[1]))]
    if len(shares)<k:
    #not enough shares
        return
    message=''
    #each run through this loop produces another character of the secret
    for byteshares in charactershares:
        xvals=[x[0] for x in byteshares]
        yvals=[x[1] for x in byteshares]
        secretsum=0
        for j in range(k):
            numerator=yvals[j]
            denominator=1
            for l in range(k):
                if l!=j:
                    numerator=(numerator*xvals[l])%p
                    denominator=(denominator*(xvals[l]-xvals[j]))%p
            secretsum+=divmod(numerator,denominator,p)

        message=message+(chr(secretsum%p))

    return message



#for creating secret shares of number only
#S is an int here
def get_shares(k,n,S,prime=None):

    if prime is None:
    #TODO: make big prime P as a basis for working in Zp
        candidates=list(filter(lambda x:x>S,prime_sieve(S*10)))
        #candidates are all primes between S and 10S
        topprime=choice(candidates)
    else:
        topprime=prime
    
    #want to create a polynomial of degree k-1 so we need k constants
    #we dissallow coefficients of 0 for simplicity, we must avoid zero in
    #the highest order coefficient
    coefficients=[S]
    coefficients.extend(randint(1,topprime-1) for _ in range(k-1))
    #confirm that the secret is indeed contained as the
    #constant in the resulting polynomial
    assert S==evaluate_polynomial(0,coefficients)%topprime

    used_xvals=[]
    found_yvals=[]

    for i in range(n):
        xval=randint(1,topprime-1)
        while xval in used_xvals:
            #theoretically can be infinite, maybe do something about that,
            #call needs to be malfromed for that to happen though
            xval=randint(1,topprime-1)
        used_xvals.append(xval)
        found_yvals.append(evaluate_polynomial(xval,coefficients)%topprime)
    shares=[(used_xvals[i],found_yvals[i]) for i in range(n)]
    return topprime,shares



def evaluate_polynomial(x,coefficients):
    output=0
    for i in range(len(coefficients)):
        output+=coefficients[i]*x**i
    return output


def divmod(a,b,p):
    #Division in the module P
    #adapted from wikipedia psuedocode
    s=0
    s_prev=1
    t=1
    t_prev=0
    r=b
    r_prev=p
    while r!=0:
        quotient=r_prev//r
        r_prev,r=r,r_prev - quotient*r
        s_prev,s=s,s_prev - quotient*s
        t_prev,t=t,t_prev - quotient*t
    #either s_prev or t_prev is the inverse of b
    #return a*s_prev or return a*t_prev
    return a*t_prev

def prime_sieve(limit):
    #stolen from stackexchange, well known problem of little interest
    a = [True] * limit  # Initialize the primality list
    a[0] = a[1] = False
    output=[]
    for (i, isprime) in enumerate(a):
        if isprime:
            output.append(i)
            for n in range(i*i, limit, i):     # Mark factors non-prime
                a[n] = False
    return output



def combine(k,n,p,shares):
    if len(shares)<k:
    #not enough shares
        return
    topprime=p
    xvals=[x[0] for x in shares]
    yvals=[x[1] for x in shares]
    secretsum=0
    for j in range(k):
        numerator=yvals[j]
        denominator=1
        for l in range(k):
            if l!=j:
                numerator=(numerator*xvals[l])%p
                denominator=(denominator*(xvals[l]-xvals[j]))%p
        secretsum+=divmod(numerator,denominator,p)
    return secretsum%p

testsecret=921

testprime=13
print(5*divmod(3,5,testprime) % testprime)
p,shares=get_shares(3,5,testsecret)
for share in shares:
    print(share)

print('testing numeric secret sharer')
combinedsecret=combine(3,5,p,shares)
print('original secret was:',testsecret)
print('extracted secret was:',combinedsecret)

testsecret="hello world!" 
p,shares=get_byte_shares(3,5,testsecret)
print('testing string secret sharer')
print('len(shares):',len(shares))
combinedsecret=combine_byte_shares(3,5,p,shares)
print('original secret was:',testsecret)
print('extracted secret was:',combinedsecret)
