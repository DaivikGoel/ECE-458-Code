from random import randint
import hashlib
import sys
from sympy import mod_inverse

if sys.version_info < (3, 6):
    import sha3

p = 168199388701209853920129085113302407023173962717160229197318545484823101018386724351964316301278642143567435810448472465887143222934545154943005714265124445244247988777471773193847131514083030740407543233616696550197643519458134465700691569680905568000063025830089599260400096259430726498683087138415465107499

sks = [432398415306986194693973996870836079581453988813,165849943586922055423650237226339279137759546603,627658512551971075308886219669315148725310346887 ]

g = 94389192776327398589845326980349814526433869093412782345430946059206568804005181600855825906142967271872548375877738949875812540433223444968461350789461385043775029963900638123183435133537262152973355498432995364505138912569755859623649866375135353179362670798771770711847430626954864269888988371113567502852

q = 959452661475451209325433595634941112150003865821


sk1 = 432398415306986194693973996870836079581453988813
sk2 = 165849943586922055423650237226339279137759546603
sk3 = 627658512551971075308886219669315148725310346887

amnt0, amnt1, amnt2, amnt3 = 1, 2, 3, 4

pk = []

def generate_public_key(g, sk, p):
    print("GENRATING PUBLIC KEY")
    
    output = pow(g, sk, p)
    return output

def question1(g, p, sks): 
    for sk in sks:  
        pki = generate_public_key(g, sk, p)
        pk.append(pki)
        #print(sk, pki)
    #print(pk)

def question2():
    
    hashobj = hashlib.sha3_224()
    
    
    # providing the input to the hashing algorithm.

    integer = int(input("PLEASE ENTER YOUR INTEGER: "))
    integer = hex(integer)
    integer = integer[2:]
    integer = bytes(integer, encoding='utf-8')

    hashobj.update(integer)
    hashed = str(hashobj.hexdigest())

    print(bin(int(hashed, 16))[2:])

def question3(pk1, pk2, amnt):
    generate_message(pk1,pk2,amnt)


def generate_signature(message, p, q, g, sk):
    k = randint(0, p-1)

    hashobj = hashlib.sha3_224()
    # hashed_num = int.from_bytes(hashlib.sha3_224(message.encode()).digest(), byteorder='big' )


    integer = hex(message)
    integer = integer[2:]
    integer = bytes(integer, encoding='utf-8')

    hashobj.update(integer)
    hashed = str(hashobj.hexdigest())
    hashed_num = int(hashed, 16)

    print("hashed_num ", hashed_num)
    
    # secret key sk1 ~ x
    print('secret key ', sk)
    y = pow(g, sk, p) # public key
    print('public key ', y)

    r = pow(g, k, p)


    # hashed_num = (sk1 * r + k * s) % q
    s = ((hashed_num - sk * r)  * mod_inverse(k, q)) % q

    print((hashed_num - sk * r)  * mod_inverse(k, q))
    print('r ', r)
    print('s ', s)
    return hashed_num, r, s, y

    # ex:
    # print("s ", ((22 - 5 * 3) * mod_inverse(8, 11)) % 11)

    # obj_sha3_224 = hashlib.sha3_224(message.encode()).digest()
    # print("sha3_224 hash in hex: ", obj_sha3_224)


def verify_signature(hashed_message, r, s, g, p, q, pk):
    if r < 0 or r > p or s < 0 or s > p:
        print ("verification rejected ")
        return False

    # u = hashed_num * s inverse mod q, 
    # and v = -r * s inverse mod q
    s1 = mod_inverse(s, q)
    u = hashed_message * mod_inverse(s, q) % q
    v = (-r * s1) % q

    print("u: ", u)
    print("v: ", v)

    arg1 = pow(g, u, p)
    arg2 = pow(pk, v, p)

    w = arg1 * arg2
    w = pow(w, 1, p)
    print("w", w)

    if r == w:
        print("verification succesful ")
        return True


def generate_message(pk1, pk2, amnt):
    pk1= bin(pk1)[2:401]
    pk2 = bin(pk2)[2:401]
    amnt = bin(amnt)[2:] if amnt != 1 else "01"

    m1 = int(pk1 + pk2 + amnt, 2)
    print(m1)

def selector():
    selected = input("WHICH QUESTION DO YOU WANT: ")

    if selected == '1':
        question1(g,p,sks)
    elif selected == '2':
        question2()
    elif selected =='3':
        question1(g,p,sks)
        question3(pk[0], pk[1], 2)
    elif selected =='4':
        hash_msg, generated_r, generated_s, y = generate_signature(45, p, q, g, sk1)
        # generate_signature(45, 23, 11, 2, 5)

        verify_signature(hash_msg, generated_r , generated_s, g, p, q, y)

selector()
    

