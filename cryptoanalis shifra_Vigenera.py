chastota_bukv=[]
chastota_bukv2=[]
chastota=['E', 'A', 'R', 'I', 'O', 'T', 'N', 'S', 'L', 'C', 'U', 'D', 'P', 'M', 'H', 'G', 'B', 'F', 'Y', 'W', 'K', 'V', 'X', 'Z', 'J', 'Q']#частота появления символов в нормальном тексте по убыванию
alphabet=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
print('Введите шифр')
shifr=input()
shifr=shifr.upper()#делаю все символы (шифра) заглавными
shifrs=shifr
shifr=list(shifr)
x=0
k=0
def index(shifr):
    itog=[]
    for i in range(1, len(shifr)):#Запускаю цикл который будет перебирать длину ключа от 1 до длины шифра
        group = []
        for j in range(0, len(shifr), i):#Запускаю цикл который перебирает каждый символ i-тый символ ((0, i, 2i) и тд)
            group.append(shifr[j])# добавляю все символы
        count=0
        for k in alphabet:#Перебираю алфавит и по формуле индекс совпадений считаю его
            count += (group.count(k) * (group.count(k) - 1)) / (len(group) * (len(group) - 1))
        itog.append(count)#добавил все индексы совпадений
    max_itog=[]
    z=0
    for i in itog:#В данном цикле оставляю только самые близкие значения к индексу совпадений в английском языке
        if i>0.06 and i< 0.06777:
            max_itog.append(i)
            z+=1
    if z==0:
        max_itog=sorted(itog)
        max_itog=max_itog[len(shifr)-3:]
    max_index=[]
    for i in max_itog:#Получаю какому индексу совпадений соответствует длина ключа
        if i in itog:
            max_index.append(itog.index(i)+1)
    max_index=sorted(set(max_index))#сортирую возможные длины ключей по возрастанию
    gruppa=[]
    gamma=[]
    x=0
    for i in max_index:#Это цикл частотного анализа; В первом for я беру возможную длину ключа
        gamma.append('/')
        for k in range(0, int(i)):#В этом цикле я перебираю числа от нуля до длины ключа взятого в прошлом цикле
            chastota_bukv = []
            for j in range(k, len(shifr), int(i)):#Запускаю цикл который перебирает каждый символ i-тый символ ((0, i, 2i) потом (1, 1+i, 1+2i) и тд)
                gruppa.append(shifr[j])#Создаю группы каждых i-тых чисел
            for m in alphabet:#провожу частотный анализ всех букв у каждой группы
                chastota_bukv.append(gruppa.count(m))
            max_vstrecha=max(chastota_bukv)
            for j in chastota_bukv:#Смотрю наиболее частые встречающиеся символы, значит что скорее всего при осмысленном тексте это буква до шифрования была E
                if j==max(chastota_bukv) and x!=1:
                    gamma.append(alphabet[(chastota_bukv.index(j)-alphabet.index('E'))%26])
                    x+=1
            gruppa=[]
            x=0
    print('Получившаяся гамма; "/" разделены гаммы (если не удалось определить однозначно ее длину); Рядом показаны числа какой длины может быть гамма')
    print(gamma)
    print(max_index)
    print('Если вы считаете, что это самоключ по тексту, то напишите 1, если самоключ по шифру, то напишите 2')
    print('Если все хорошо напишите осмысленное значение которое может подойти под гамму')
    x=input()#Проанализировав выданные возможные гаммы пользователь пишет наиболее вероятную гамму
    #В случае если не получилось удачно расшифровать текст, то пользователь может предположить, что способ шифрование это самоключ, а не повтор ключа
    if x!='1' and x!='2':
        gamma=x
        gamma=gamma.upper()
        while len(shifr)>len(gamma):#цикл while увеличивает длину гаммы повторяя ключ, пока он не станет больше шифра
            gamma+=gamma
        if len(gamma)>len(shifr):
            k=len(gamma)-(len(gamma)-len(shifr))
            gamma=gamma[:k]#обрезаю ключ до длины исходного текста
        otvet=''
        for i in range(0, len(shifr)):#С помощью цикла for расшифрую каждый символ шифртекста
            j = i
            otvet += alphabet[(alphabet.index(shifr[i]) + 26 - alphabet.index(gamma[j])) % 26]
        return (otvet)
    if x == '1':#В случае если не получилось удачно расшифровать текст, то пользователь может предположить, что способ шифрование это самоключ, а не повтор ключа
        print(decode_texta(shifr))
    if x == '2' or k == '2':#В случае если не получилось удачно расшифровать текст, то пользователь может предположить, что способ шифрование это самоключ, а не повтор ключа
        print(decode_shifra(shifrs))
def decode_texta(shifr):#криптоанализ самоключа по открытому тексту
    for k in alphabet:#Перебор первого символа
        gamma=k
        gamma = gamma.upper()
        otvet = ''
        for i in range(0, len(shifr)):#С помощью цикла for расшифрую каждый символ шифртекста
            j = i
            otvet += alphabet[(alphabet.index(shifr[i]) + 26 - alphabet.index(gamma[j])) % 26]
            gamma += alphabet[(alphabet.index(shifr[i]) + 26 - alphabet.index(gamma[j])) % 26]#как только мы узнаем символ открытого текста увеличиваем гамму
        print(alphabet.index(k)+1, otvet)
    print('Если из выданных выражений нет подходящего, то возможно это самключ по шифру, для попытки расшифровать напишите 2')
    print('Если все хорошо напишите 3')
    k=input()
    if x == '2' or k == '2':
        print(decode_shifra(shifrs))
def decode_shifra(shifrs):#криптоанализ самоключа по шифртексту
    for k in alphabet:#Перебор первого символа
        gamma=k
        gamma += shifrs[:len(shifrs) - 1]#к первому символу гаммы прибавляется шифртекст без последнего символа
        otvet = ''
        for i in range(0, len(shifrs)):
            j = i
            otvet += alphabet[(alphabet.index(shifrs[i]) + 26 - alphabet.index(gamma[j])) % 26]#С помощью цикла for расшифрую каждый символ шифртекста
        print(alphabet.index(k)+1, otvet)
    print('Если из выданных выражений нет подходящего, то возможно это самоключ по тексту, для попытки расшифровать напишите 1')
    print('Если все хорошо и вы нашли свое выражение напишите 3')
    x=input()
    if x == '1':
        print(decode_texta(shifr))
print(index(shifr))
