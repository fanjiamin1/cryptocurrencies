from random import randint



def get_shares(k,n,S):


    #TODO: make big prime P as a basis for working in Zp
    topprime=5
    
    coefficients=[randint(1,topprime) for x in range(k)]

    used_xvals=[]
    found_yvals=[]

    for i in range(n):
        xval=randint(1,topprime-1)
        while xval in used_xvals:
            xval=randint(1,topprime-1)
        used_xvals.append(x)
        found_yvals.append(evaluate_polynomial(x,coefficients)%topprime)
    shares=[(used_xvals[i],found_yvals[i]) for i in range(n)]
    return p,shares



def evaluate_polynomial(x,coefficients):
    output=0
    for i in range(len(coefficients):
        sum+=coefficients[i]*x**i
    return output


def combine(k,n,p,shares):
    if len(shares)<k:
    #not enough shares
        return
    topprime=p
    xvals=[x[0] for x in shares]
    yvals=[x[1] for x in shares]
    secretsum=0
    sum([ 
    denominators=[yvals[j]*reduce(
                operator.mul,[xvals[i] for i in range(k) where i!=j])
                for j in range(k)
                ]
    divisors = [ reduce(operator.mul,
                [xvals[i]-xvals[j] for i in range(k) where i!=j]
                for j in range[k]]
    secretsum=sum([denominators[i]/divisors[i] for i in range(k)]

    return secretsum
        


    
