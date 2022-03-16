alphabet=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
chisla=['1','2','3','4','5','6','7','8','9', '0']
punctuation="!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
print('Введите текст')
shifr=input()
shifr=shifr.upper() #делаю все символы текста(шифра) заглавными
shifr=shifr.replace(' ','') #Удаляю пробелы
print('Введите ключ')
kluch=input()
kluch=kluch.upper() #делаю все символы ключа заглавными
print('Если Зашифровать, то напишите 1, если расшифровать, то 2')
z=int(input())
print('Выберите метод шифрования: 1 - Повтор, 2 - Самоключ по тексту, 3 - Самоключ по шифру(напишите цифру) ')
c=int(input())
for i in punctuation:#С 15 по 24 строчки удаляю все знаки пунктуации из текста(шифра) и ключа
    if i in shifr:
        shifr=shifr.replace(i,'')
    if i in kluch:
        kluch=kluch.replace(i,'')
for i in chisla:
    if i in shifr:
        shifr=shifr.replace(i,'')
    if i in kluch:
        kluch=kluch.replace(i,'')
def povtor(shifr, kluch): #шифрование путем повтора ключа
    gamma=kluch
    while len(shifr)>len(gamma):#цикл while увеличивает длину гаммы повторяя ключ, пока он не станет больше открытого текста
        gamma+=gamma
    if len(gamma)>len(shifr):
        k=len(gamma)-(len(gamma)-len(shifr))
        gamma=gamma[:k] #обрезаю ключ до длины исходного текста
    otvet = ''
    for i in range (0, len(shifr)):#С помощью цикла for шифрую каждый символ исходного текста
        j=i
        otvet+=alphabet[(alphabet.index(shifr[i])+alphabet.index(gamma[j]))%26]
    return(otvet)
def samokluch_po_teksty(shifr, kluch): #шифрование с помощью самоключа по открытому тексту
    gamma=kluch[0]#Гамма получает первый символ ключа
    gamma+=shifr[:len(shifr)-1]#к первому символу гаммы прибавляется открытый текст без последнего символа
    otvet = ''
    for i in range(0, len(shifr)):#С помощью цикла for шифрую каждый символ исходного текста
        j = i
        otvet += alphabet[(alphabet.index(shifr[i]) + alphabet.index(gamma[j])) % 26]
    return (otvet)
def samokluch_shifru(shifr, kluch):  #шифрование с помощью самоключа по шифртексту
    gamma=kluch[0]#Гамма получает первый символ ключа
    for i in range(0, len(shifr)-1):#гамма строится постепенно получая символы уже зашифрованного текста
        j = i
        gamma+= alphabet[(alphabet.index(shifr[i]) + alphabet.index(gamma[j])) % 26]
    otvet = ''
    for i in range(0, len(shifr)):#С помощью цикла for шифрую каждый символ исходного текста
        j = i
        otvet += alphabet[(alphabet.index(shifr[i]) + alphabet.index(gamma[j])) % 26]
    return (otvet)
def decode_povtora(shifr, kluch):#расшифровака текста, зашифрованного повтором
    gamma=kluch#Гамме присваивается ключ
    while len(shifr)>len(gamma): #цикл while увеличивает длину гаммы повторяя ключ, пока он не станет больше шифра
        gamma+=gamma
    if len(gamma)>len(shifr):
        k=len(gamma)-(len(gamma)-len(shifr))
        gamma=gamma[:k]#обрезаю ключ до длины исходного текста
    otvet=''
    for i in range(0, len(shifr)):#С помощью цикла for расшифрую каждый символ шифртекста
        j = i
        otvet += alphabet[(alphabet.index(shifr[i]) + 26 - alphabet.index(gamma[j])) % 26]
    return (otvet)
def decode_tekst(shifr, kluch):
    gamma = kluch[0]#Гамма получает первый символ ключа
    otvet=''
    for i in range(0, len(shifr)):#С помощью цикла for расшифрую каждый символ шифртекста
        j = i
        otvet += alphabet[(alphabet.index(shifr[i]) + 26 - alphabet.index(gamma[j])) % 26]
        gamma+= alphabet[(alphabet.index(shifr[i]) + 26 - alphabet.index(gamma[j])) % 26]#как только мы узнаем символ открытого текста увеличиваем гамму
    return otvet
def decode_shifru(shifr, kluch):
    gamma=kluch[0]#Гамма получает первый символ ключа
    gamma +=shifr[:len(shifr)-1]#к первому символу гаммы прибавляется шифртекст без последнего символа
    otvet = ''
    for i in range(0, len(shifr)):#С помощью цикла for расшифрую каждый символ шифртекста
        j = i
        otvet += alphabet[(alphabet.index(shifr[i]) + 26 - alphabet.index(gamma[j])) % 26]
    return otvet
if z==1:
    if c==1:
        print(povtor(shifr, kluch))
    if c==2:
        print(samokluch_po_teksty(shifr, kluch))
    if c==3:
        print(samokluch_shifru(shifr, kluch))
if z==2:
    if c==1:
        print(decode_povtora(shifr, kluch))
    if c==2:
        print(decode_tekst(shifr, kluch))
    if c==3:
        print(decode_shifru(shifr, kluch))
