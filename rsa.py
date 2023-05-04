import pickle
import random
import math
def rash_evklid(a,b):
    x1=0
    x2=1
    y2=0
    y1=1
    while b>0:
        q=a//b
        r=a-q*b
        x=x2-q*x1
        y=y2-q*y1
        a=b
        b=r
        x2=x1
        x1=x
        y2=y1
        y1=y
    return x2

def exponentiation_modulo(a,k,n):
    kbin=str(bin(k)[2:])
    kbin=kbin[::-1]
    b=1
    if k==0:
        return b
    A=a
    if int(kbin[0])==1:
        b=a
    for i in range(1,len(kbin)):
        A=(A**2) % n
        if int(kbin[i])==1:
            b=(A*b)%n
    return b

def is_prime(n):
    if n==2:
        return True
    if n<2 or n%2==0:
        return False
    check=n-2
    if check<=20:
        check=check-2
    else:
        check=20
    for i in range(1,check):
        a=random.randint(2,n-1)
        r=exponentiation_modulo(a,n-1,n)
        if r!=1:
            return False
    return True

def generate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def n_bit_prime(length):
    while not is_prime(p := generate(length)):
        pass
    return p
def keygen(choice,plen,qlen):
    if choice=="1":
        p=0
        q=0
        while p==q:
            p = n_bit_prime(plen)
            q = n_bit_prime(qlen)
    elif choice=="2":
        p = int(input("Введите p\n"))
        q = int(input("Введите q\n"))
    else:
        return "Введено непонятное значение"
    if p==q and is_prime(p) and is_prime(q):
        return "p и q должный быть простыми и разными числами"
    n=p*q
    phi=(abs(p)-1)*(abs(q)-1)
    if choice=="1":
        e=random.randrange(1,phi)
        while math.gcd(e, phi) != 1:
            e = random.randrange(1, phi)
    elif choice=="2":
        e=int(input("Введите e\n"))
    else:
        return "Введено непонятное значение"
    d=rash_evklid(e,phi)
    if d<0:
        d+=phi
    print(f"Открытый ключ:{e,n}")
    print(f"Закрытый ключ:{d,n}")
    return [[e,n],[d,n]]

def encrypt(text,e,n):
    block_size = math.floor(math.log(n, 2))
    result=[]
    binary = "".join(map("{:08b}".format, text))
    if len(binary) % block_size != 0:
        binary=binary[::-1]
        binary+='0'*(block_size-len(binary)%block_size)
        binary=binary[::-1]
    for i in range(0,len(binary),block_size):
        a=int(binary[i:i+block_size],2)
        c=exponentiation_modulo(a,e,n)
        result.append(c)
    return result

def decrypt(text,d,n):
    block_size = math.floor(math.log(n, 2))
    result=[]
    for i in range(0, len(text)):
        a = exponentiation_modulo(text[i], d, n)
        result.append(a)

    binary_text=''
    for i in range(1,len(result)):
        check = bin(result[i])[2:]
        while len(check) < block_size:
            check = check[::-1]
            check += '0'
            check = check[::-1]
        binary_text += check
    binary_text=bin(result[0])[2:]+binary_text
    while len(binary_text)%8!=0:
        binary_text = binary_text[::-1]
        binary_text += '0'
        binary_text = binary_text[::-1]
    end=[]
    for i in range(len(binary_text),0,-8):
        end.append(int(binary_text[i-8:i], 2))
    return end


def main_file(path,n,choice):
    if choice=="1":
        with open(path, "rb") as file:
            text = file.read()
    elif choice=="2":
        with open(path, "rb") as file:
            text=pickle.load(file)
    if path.rfind("\\") == -1:
        file_path = path[:path.find(".")] + "_" + path[path.find(".") + 1:]
    else:
        file_path = path[path.rfind("\\") + 1:path.find(".")] + "_" + path[path.find(".") + 1:]
    if choice == "1":
        e=pair[0][0]
        result = encrypt(text, e, n)
    elif choice == "2":
        d = pair[1][0]
        result=decrypt(text,d,n)
    else:
        return "Выбрано некорректное значение"
    if choice == "1":
        with open(f'{file_path}' + '.rsa', "wb") as file:
            pickle.dump(result, file)
        return "В папке с программой появился новый файл"
    elif choice=="2":
        rash = file_path[file_path.find("_") + 1:]
        full = b''
        for i in range(len(result) - 1, -1, -1):
            full += result[i].to_bytes(1, 'big')
        with open(f'{file_path[:-4]}input' + f'.{rash[:-4]}', "wb") as file:
            file.write(full)
        return "В папке с программой появился новый файл"
    else:
        return "Выбрано некорректное значение"

def main_text(text,choice,n):
    if choice=="1":
        text=bytes(text,"utf-8")
        return encrypt(text,pair[0][0],n)
    elif choice=="2":
        text=list(map(int,list(text.split())))
        answer=decrypt(text,pair[1][0],n)
        end=''
        for i in answer:
            end+=chr(i)
        return end[::-1]
    else:
        return "Выбрано некорректное значение"
pair=[]
choice2=(input("Если хотите сгенерировать ключ, нажмите 1\nЕсли хотите ввести p и q, то нажмите 2\n"))
if choice2=="1":
    p_ran=int(input("Введите длину p\n"))
    q_ran=int(input("Введите длину q\n"))
    pair = keygen(choice2, p_ran, q_ran)
    n = pair[0][1]
elif choice2=="2":
    p_ran = 0
    q_ran = 0
    pair = keygen(choice2, p_ran, q_ran)
    n = pair[0][1]
else:
    print("Введено некорректное значение")
    exit(-1)
while True:
    choice3=input("Если хотите использовать файл, то нажмите 1\nЕсли хотите ввести текст, то нажмите 2\n")
    if choice3=="1":
        path=input("Введите путь до файла:\n")
        choice=input("1 - Зашифровать\n2 - Расшифровать\n")
        ch=input("Если вы хотите использовать сгенерированный ключ, то нажмите 1, иначе любое число\n")
        if ch!="1":
            closee=input("Введите закрытый ключ:\n")
            opene=input("Введите открытый ключ\n")
            pair[0]=list(map(int,list(opene.split())))
            pair[1]=list(map(int,list(closee.split())))
            n = pair[0][1]
        print(main_file(path,n,choice))
    if choice3=="2":
        choice = input("1 - Зашифровать\n2 - Расшифровать\n")
        ch = input("Если вы хотите использовать сгенерированный ключ, то нажмите 1, иначе любое число\n")
        if ch != "1":
            closee = input("Введите закрытый ключ:\n")
            opene = input("Введите открытый ключ\n")
            pair[0] = list(map(int, list(opene.split())))
            pair[1] = list(map(int, list(closee.split())))
            n = pair[0][1]
        if choice=="1":
            path = input("Введите текст для зашифрования\n")
        elif choice=="2":
            path = input("Введите числовую последовательность через пробел для расшифрования\n")
        else:
            break
        print(main_text(path,choice,n))
    a=input("Если хотите завершить, то нажмите 1\n")
    if a=="1":
        break
