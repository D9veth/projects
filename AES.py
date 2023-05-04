import binascii
Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)
rounds_by_key_size = {16: 10, 24: 12, 32: 14}

r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)

inv_sbox = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

def mul_by_02(num):
    """ Умножение на {02} в GF(2^8)"""
    if num < 0x80:
        res = (num << 1)
    else:
        res = (num << 1) ^ 0x11B
    return res
def mul_by_03(num):
    """ Умножение на {03} в GF(2^8)"""
    return (mul_by_02(num) ^ num)

def bytes2matrix(text):
    """Разбивает байтовую последовательность на матрицу 4x4"""
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def mul_by_09(num):
    """ Умножение на {09} в GF(2^8)"""
    return mul_by_02(mul_by_02(mul_by_02(num))) ^ num


def mul_by_0b(num):
    """ Умножение на {0b} в GF(2^8)"""
    return mul_by_02(mul_by_02(mul_by_02(num))) ^ mul_by_02(num) ^ num


def mul_by_0d(num):
    """ Умножение на {0d} в GF(2^8)"""
    return mul_by_02(mul_by_02(mul_by_02(num))) ^ mul_by_02(mul_by_02(num)) ^ num

def xor_bytes(a, b):
    """Операция XOR двух последовательностей"""
    return bytes(i^j for i, j in zip(a, b))


def mul_by_0e(num):
    """ Умножение на {0e} в GF(2^8)"""
    return mul_by_02(mul_by_02(mul_by_02(num))) ^ mul_by_02(mul_by_02(num)) ^ mul_by_02(num)

def matrix2bytes(matrix):
    """Превращает матрицу в байтовую последовательность"""
    return bytes(sum(matrix, []))

def sub_bytes(s):
    """Преобразование Subbytes()"""
    for i in range(4):
        for j in range(4):
            s[i][j] = Sbox[s[i][j]]
    return s

def inv_sub_bytes(s):
    """Преобразование InvSubbytes()"""
    for i in range(4):
        for j in range(4):
            s[i][j] = inv_sbox [s[i][j]]
    return s

def shift_rows(s):
    """Преобразование Shiftrows()"""
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]
    return s

def inv_shift_rows(s):
    """Преобразование Invshiftrows()"""
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]
    return s

def mix_columns(state):
    """Преобразование MixColumns()"""
    state2=[x[:] for x in state]
    for i in range(4):
        s0 = mul_by_02(state[i][0]) ^ mul_by_03(state[i][1]) ^ state[i][2] ^ state[i][3]
        s1 = state[i][0] ^ mul_by_02(state[i][1]) ^ mul_by_03(state[i][2]) ^ state[i][3]
        s2 = state[i][0] ^ state[i][1] ^ mul_by_02(state[i][2]) ^ mul_by_03(state[i][3])
        s3 = mul_by_03(state[i][0]) ^ state[i][1] ^ state[i][2] ^ mul_by_02(state[i][3])
        state2[i][0] = s0
        state2[i][1] = s1
        state2[i][2] = s2
        state2[i][3] = s3
    return state2

def inv_mix_columns(state):
    """Преобразование InvMixColumns()"""
    state2=[x[:] for x in state]
    for i in range(4):
        s0 = mul_by_0e(state[i][0]) ^ mul_by_0b(state[i][1]) ^ mul_by_0d(state[i][2]) ^ mul_by_09(state[i][3])
        s1 = mul_by_09(state[i][0]) ^ mul_by_0e(state[i][1]) ^ mul_by_0b(state[i][2]) ^ mul_by_0d(state[i][3])
        s2 = mul_by_0d(state[i][0]) ^ mul_by_09(state[i][1]) ^ mul_by_0e(state[i][2]) ^ mul_by_0b(state[i][3])
        s3 = mul_by_0b(state[i][0]) ^ mul_by_0d(state[i][1]) ^ mul_by_09(state[i][2]) ^ mul_by_0e(state[i][3])
        state2[i][0] = s0
        state2[i][1] = s1
        state2[i][2] = s2
        state2[i][3] = s3
    return state2


def add_round_key(s, k):
    """Преобразование AddRoundKey()"""
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]
    return s

def key_expansion(key):
    """Развертывание раундовых ключей"""
    assert len(key) in rounds_by_key_size
    Nr=rounds_by_key_size[len(key)]
    i=len(key)//4
    Nk=len(key)//4
    key_schedule = list(bytes2matrix(key))
    while (i<4*(Nr+1)):
        word = list(key_schedule[-1])
        if i%Nk==0:
            word.append(word.pop(0))
            word = [Sbox[b] for b in word]
            word[0] ^= r_con[i//Nk]
        elif Nk>6 and i%Nk==4:
            word = [Sbox[b] for b in word]
        word = xor_bytes(word, key_schedule[-Nk])
        i+=1
        key_schedule.append(word)
    return [key_schedule[4*i : 4*(i+1)] for i in range(len(key_schedule) // 4)]

def encrypt(text,key):
    """Зашифрование"""
    assert len(text) == 16
    plain_state = bytes2matrix(text)
    key_matrix=key_expansion(key)
    assert len(key) in rounds_by_key_size
    Nr = rounds_by_key_size[len(key)]
    plain_state=add_round_key(plain_state,key_matrix[0])
    for i in range(1,Nr):
        plain_state=sub_bytes(plain_state)
        plain_state=shift_rows(plain_state)
        plain_state=mix_columns(plain_state)
        plain_state=add_round_key(plain_state,key_matrix[i])
    plain_state = sub_bytes(plain_state)
    plain_state = shift_rows(plain_state)
    plain_state = add_round_key(plain_state, key_matrix[-1])

    return matrix2bytes(plain_state)

def decrypt(ciphertext,key):
    """Расшифрование"""
    assert len(ciphertext) == 16
    cipher_state = bytes2matrix(ciphertext)
    key_matrix = key_expansion(key)
    assert len(key) in rounds_by_key_size
    Nr = rounds_by_key_size[len(key)]
    cipher_state = add_round_key(cipher_state, key_matrix[-1])
    cipher_state = inv_shift_rows(cipher_state)
    cipher_state = inv_sub_bytes(cipher_state)
    for i in range(Nr-1,0,-1):
        cipher_state = add_round_key(cipher_state, key_matrix[i])
        cipher_state = inv_mix_columns(cipher_state)
        cipher_state = inv_shift_rows(cipher_state)
        cipher_state = inv_sub_bytes(cipher_state)

    cipher_state = add_round_key(cipher_state, key_matrix[0])
    return matrix2bytes(cipher_state)

def main(path,key,choice):
    with open(path, "rb") as file:
        text =file.read()
    print(text)
    text = [text[i:i + 16] for i in range(0, len(text), 16)]
    if path.rfind("\\") == -1:
        file_path = path[:path.find(".")] + "_" + path[path.find(".") + 1:]
    else:
        file_path = path[path.rfind("\\") + 1:path.find(".")] + "_" + path[path.find(".") + 1:]
    counter=0
    while len(text[-1])<15:
        text[-1]+=b'\x00'
        counter+=1
    result=[]
    if len(text[-1])==15:
        text[-1]+=counter.to_bytes(1,byteorder="big")
    key=binascii.unhexlify(key)
    if choice=="1":
        for i in text:
            result.append(encrypt(i,key))
    elif choice=="2":
        for i in text:
            result.append(decrypt(i,key))
    else:
        return "Выбрано некорректное значение"
    file.close()
    if choice=="1":
        with open(f'{file_path}' + '.aes', "wb") as file:
            for i in range(len(result)):
                file.write(result[i])
        return "В папке с программой появился новый файл"
    elif choice=="2":
        rash=file_path[file_path.find("_")+1:]
        a=int.from_bytes(result[-1][15:],"big")
        if 0<=a<=15:
            result[-1]=result[-1][:-(a+1)]
        with open(f'{file_path[:-4]}input' + f'.{rash[:-4]}', "wb") as file:
            for i in range(len(result)):
                file.write(result[i])
        return "В папке с программой появился новый файл"
    else:
        return "Выбрано некорректное значение"

path=input("Введите путь до файла:\n")
key=input("Введите ключ:\n")
choice=input("1 - Зашифровать\n2 - Расшифровать\n")
print(main(path,key,choice))



#256#a=(encrypt(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF',b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'))
#192#a=(encrypt(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF',b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'))
#128#a=(encrypt(b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xAA\xBB\xCC\xDD\xEE\xFF',b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'))

#a=(decrypt(b'\x8e\xa2\xb7\xca\x51\x67\x45\xbf\xea\xfc\x49\x90\x4b\x49\x60\x89',b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'))
#a=(decrypt(b'\xdd\xa9\x7c\xa4\x86\x4c\xdf\xe0\x6e\xaf\x70\xa0\xec\x0d\x71\x91',b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17'))
#a=(decrypt(b'i\xc4\xe0\xd8j{\x040\xd8\xcd\xb7\x80p\xb4\xc5Z',b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'))

# b=""
# for i in a:
#     b+=hex(int(i))[2:]
# print(b)