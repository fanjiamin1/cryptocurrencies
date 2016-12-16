from random import randint
from functools import reduce



def get_shares(k,n,S):

    #TODO: make big prime P as a basis for working in Zp
    topprime=10009
    
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

            
    #the below should be equivalent to the above arithmetic
    denominators=[yvals[j]*reduce
                 (
                    lambda x,y: x*y,
                    [xvals[i] for i in range(k) if i!=j]
                 )
                for j in range(k)
                ]
    divisors = [ reduce(
                            lambda x,y: x*y,
                            [xvals[i]-xvals[j] for i in range(k) if i!=j]
                       )
                for j in range(k)
                ]
    secretsum=sum([divmod(denominators[i],divisors[i],p) for i in range(k)])

    return secretsum%p
        
testsecret=9001

testprime=13
print(5*divmod(3,5,testprime) % testprime)
p,shares=get_shares(3,5,testsecret)
for share in shares:
    print(share)

combinedsecret=combine(3,5,p,shares)
print('original secret was:',testsecret)
print('extracted secret was:',combinedsecret)

    
