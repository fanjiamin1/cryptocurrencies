import random


TOP_PRIME_PER_BYTE=251


class Polynomial(list):
    def __call__(self, x):
        return sum(
                    coefficient*(x**power)
                    for power, coefficient in enumerate(self)
                  )

    def __str__(self):
        return " + ".join(
                           str(coefficient) + "*x^" + str(power)
                           for power, coefficient in enumerate(self)
                         )

    def __repr__(self):
        return "Polynomial({})".format(super(Polynomial, self).__repr__())


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
        if secret_number>TOP_PRIME_PER_BYTE:
            raise ValueError('Character:',character,'is not supported, it has an order over 251')
        #want to create a polynomial of degree k-1 so we need k constants
        #we dissallow coefficients of 0 for simplicity, we must avoid zero in
        #the highest order coefficient
        polynomial = Polynomial([secret_number])
        polynomial.extend(random.randint(1,topprime-1) for _ in range(k-1))
        #confirm that the secret is indeed contained as the
        #constant in the resulting polynomial
        assert secret_number==polynomial(0)%topprime

        used_xvals=[]
        found_yvals=[]

        for i in range(n):
            xval=random.randint(1,topprime-1)
            while xval in used_xvals:
                #theoretically can be infinite, maybe do something about that,
                #call needs to be malfromed for that to happen though
                xval=random.randint(1,topprime-1)
            used_xvals.append(xval)
            found_yvals.append(polynomial(xval)%topprime)
        #add the shares
        charactershares.append([(used_xvals[i],found_yvals[i]) for i in range(n)])
    #charactershares now contains len(S) lists of n shares each
    #each share is now a list of tuples, one for each letter of the secret message

    shares=[ list(map(lambda x:x[i],charactershares)) for i in range(n)]



    #shares has n lists, each containing len(S) tuples, which are one users keys for each byte
    return topprime,shares

#takes in shares in the same format as get_shares outputs
#outputs the secret string
def combine_byte_shares(k,p,shares):
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
            secretsum+=modular_division(numerator,denominator,p)

        message=message+(chr(secretsum%p))

    return message



#for creating secret shares of number only
#S is an int here
def get_shares(k,n,S,prime=None):

    if prime is None:
    #TODO: make big prime P as a basis for working in Zp
        candidates=list(filter(lambda x:x>S,prime_sieve(S*10)))
        #candidates are all primes between S and 10S
        topprime=random.choice(candidates)
    else:
        topprime=prime

    #want to create a polynomial of degree k-1 so we need k constants
    #we dissallow coefficients of 0 for simplicity, we must avoid zero in
    #the highest order coefficient
    polynomial = Polynomial([S])
    polynomial.extend(random.randint(1,topprime-1) for _ in range(k-1))
    #confirm that the secret is indeed contained as the
    #constant in the resulting polynomial
    assert S==polynomial(0)%topprime

    used_xvals=[]
    found_yvals=[]

    for i in range(n):
        xval=random.randint(1,topprime-1)
        while xval in used_xvals:
            #theoretically can be infinite, maybe do something about that,
            #call needs to be malfromed for that to happen though
            xval=random.randint(1,topprime-1)
        used_xvals.append(xval)
        found_yvals.append(polynomial(xval)%topprime)
    shares=[(used_xvals[i],found_yvals[i]) for i in range(n)]
    return topprime,shares



def modular_division(a, b, n):
    """Division modulo n.

    Adapted from Wikipedia pseudo-code.

    Only returns number relevant to the secret sharing process
    """
    s = 0
    s_prev = 1
    t = 1
    t_prev = 0
    r = b
    r_prev = n
    while r != 0:
        quotient = r_prev//r
        r_prev, r = r, r_prev - quotient*r
        s_prev, s = s, s_prev - quotient*s
        t_prev, t = t, t_prev - quotient*t
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



def combine(k,p,shares):
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
        secretsum+=modular_division(numerator,denominator,p)
    return secretsum%p














testsecret=921

testprime=13
print(5*modular_division(3,5,testprime) % testprime)
p,shares=get_shares(3,5,testsecret)
for share in shares:
    print(share)

print('testing numeric secret sharer')
combinedsecret=combine(3,p,shares)
print('original secret was:',testsecret)
print('extracted secret was:',combinedsecret)

testsecret="hello world!"
p,shares=get_byte_shares(3,5,testsecret)
print('testing string secret sharer')
print('len(shares):',len(shares))
combinedsecret=combine_byte_shares(3,p,shares)
print('original secret was:',testsecret)
print('extracted secret was:',combinedsecret)
