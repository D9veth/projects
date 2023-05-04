
def rational_to_contfrac(x,y):
    a = x//y
    pquotients = [a]
    while a * y != x:
        x,y = y,x-a*y
        a = x//y
        pquotients.append(a)
    return pquotients


def is_perfect_square(n):
    if n < 0:
        return -1
    else:
        for i in range(n + 1):
            i2 = i * i
            if i2 == n:
                return i
            elif i2 > n:
                return -1
    return -1

def convergents_from_contfrac(frac):
    convs = []
    for i in range(len(frac)):
        convs.append(contfrac_to_rational(frac[0:i]))
    return convs

def contfrac_to_rational (frac):
    if len(frac) == 0:
        return (0,1)
    num = frac[-1]
    denom = 1
    for i in range(-2,-len(frac)-1,-1):
        num, denom = frac[i]*num+denom, num
    return (num,denom)

def wiener(e,n):
    frac=rational_to_contfrac(e,n)
    convergents=convergents_from_contfrac(frac)
    for (k,d) in convergents:
        if k!=0 and (e*d-1)%k ==0:
            phi=((e*d-1)//k)
            s=n-phi+1
            discrim=s*s-4*n
            if discrim>=0:
                t=is_perfect_square(discrim)
                if t!=-1 and (((-s)+t)/2)*(((-s) - t) / 2)==n:
                    return f"Закрытый ключ{d,n}"
e=int(input("Введите e\n"))
n=int(input("Введите n\n"))
print(wiener(e, n))



#print(wiener(1073780833, 1220275921))
#print(wiener(17993, 90581))
