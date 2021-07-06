from random import randint
import hashlib
import sys
from sympy import mod_inverse
import datetime

if sys.version_info < (3, 6):
    import sha3

p = 168199388701209853920129085113302407023173962717160229197318545484823101018386724351964316301278642143567435810448472465887143222934545154943005714265124445244247988777471773193847131514083030740407543233616696550197643519458134465700691569680905568000063025830089599260400096259430726498683087138415465107499

sks = [432398415306986194693973996870836079581453988813,165849943586922055423650237226339279137759546603,627658512551971075308886219669315148725310346887 ]

g = 94389192776327398589845326980349814526433869093412782345430946059206568804005181600855825906142967271872548375877738949875812540433223444968461350789461385043775029963900638123183435133537262152973355498432995364505138912569755859623649866375135353179362670798771770711847430626954864269888988371113567502852

q = 959452661475451209325433595634941112150003865821


sk1 = 432398415306986194693973996870836079581453988813
sk2 = 165849943586922055423650237226339279137759546603
sk3 = 627658512551971075308886219669315148725310346887

amnt= [1, 2, 3, 4]
hashobj = hashlib.sha3_224()
#primary key array. Will be populated after question1
pk = []

def generate_public_key(g, sk, p):
    #print("GENRATING PUBLIC KEY")
    #pow does gives us g ^sk %p 
    output = pow(g, sk, p)
    return output

def question1(g, p, sks): 
    for sk in sks:  
        #goes through all secret keys and generates public key
        pki = generate_public_key(g, sk, p)
        pk.append(pki)
        #print(sk, pki)
    #print(pk)

def question2(integer):
    #converts integer into int and then hex. We then remove the leading zeroes in the hex. 
    integer = int(integer)
    integer = hex(integer)
    integer = integer[2:]
    integer = bytes(integer, encoding='utf-8')
    #From there we encode it into bytes and hash the integer
    hashobj.update(integer)
    hashed = str(hashobj.hexdigest())

    #print(bin(int(hashed, 16))[2:])

    #we return the value in binary
    return bin(int(hashed, 16))[2:]

def question3(pk1, pk2, amnt):
    #calls the generate message function to generate the concatenated message
    print(generate_message(pk1,pk2,amnt))


def generate_signature(message, p, q, g, sk):
    #get random k in between 0 and p
    k = randint(0, p-1)


    #convert message into hex and then bytes
    integer = hex(message)
    integer = integer[2:]
    integer = bytes(integer, encoding='utf-8')

    #hash the message
    hashobj.update(integer)
    hashed = str(hashobj.hexdigest())
    #convert from hex string to int
    hashed_num = int(hashed, 16) #this is our h(m)
    

    
    y = pow(g, sk, p) # public key
    #print('public key ', y)

    r = pow(g, k, p) #first integer of signature paur


    # hashed_num = (sk1 * r + k * s) % q
    s = ((hashed_num - sk * r)  * mod_inverse(k, q)) % q #second half of signature pair

    #print((hashed_num - sk * r)  * mod_inverse(k, q))
    print('r ', r)
    print('s ', s)
    #send signature pair and publick key abck 
    return hashed_num, r, s, y



def verify_signature(hashed_message, r, s, g, p, q, pk):
    #check if values fall in expected rangers
    if r < 0 or r > p or s < 0 or s > p:
        print ("verification rejected ")
        return False



    s1 = mod_inverse(s, q)
    u = hashed_message * mod_inverse(s, q) % q    # u = hashed_num * s inverse mod q, 
    v = (-r * s1) % q    # and v = -r * s inverse mod q

    arg1 = pow(g, u, p) #g ^ u mod p
    arg2 = pow(pk, v, p) #pk ^ v mod p

    w = arg1 * arg2
    w = pow(w, 1, p) # g^u y^v mod p 
    #this value is our generated r
    print("w", w)
    
    #if the r is the same we can verify that we generated a valid signature
    if r == w:
        print("verification succesful ")
        return True


def find_nounce():
    found = 0

    NONCE = 0

    question1(g,p,sks) #generate the public keys

    messages = [] #save m1, m2, m3 etc
    hashed_messages = [question2(amnt[0])] #Offset by 1 as h(m0) is h(amnt0)

    for i in range(len(pk)-1):
        #create a message using primary keys
        messages.append(generate_message(pk[i], pk[i+1], amnt[i+1]))
        #create hashed message using these messages
        hashed_messages.append(question2(generate_message(pk[i], pk[i+1], amnt[i+1])))
    nonces = []

    #use this to determine length of time it took
    start_time = datetime.datetime.now()

    for i in range(2):
        #find nonce1 and nonce2
        found = 0
        NONCE = 0
        print(i)
        for y in [26,28,30,32]: #this is for testing purposes on effort required
            found = 0
            while found == 0:
                #because the array is offset by 1 in hashedmessages it represents the equation NONCE + mi + h(m i-1)
                z = NONCE + messages[i] + int(hashed_messages[i])
                #find hash of the concatenation. 

                new_hash = question2(z) #new_hash is Ti
                # since the first 24 bits aren't shown in binary representation, when the length of the new hash is exactly 24 bits short then we know we had 24 leading zeroes
                if 224 - len(new_hash) == y:
                    #if we have 24 leading zeroes we have found a nonce
                    found = 1
                    end_time = datetime.datetime.now()

                    print("elapsed time for finding nonce: ", (end_time - start_time))
                    nonces.append(NONCE)
                NONCE +=1
            
    #show both nonces
    print(nonces)


    pass

def generate_message(pk1, pk2, amnt):
    #take the primary keys, convert to binary keeping significant digits of 399, and then add the amnt to it. We then convert back into an integer
    pk1= bin(pk1)[2:401]
    pk2 = bin(pk2)[2:401]
    amnt = bin(amnt)[2:] if amnt != 1 else "01" #special case for 1.

    m1 = int(pk1 + pk2 + amnt, 2)
    return m1

def selector():
    selected = input("WHICH QUESTION DO YOU WANT: ")

    if selected == '1':
        question1(g,p,sks)
    elif selected == '2':
        question2(input("PLEASE ENTER YOUR INTEGER: "))
    elif selected =='3':
        #gets messages for both m1 and m2. Question 1 populates primary key array
        question1(g,p,sks)
        print("M1")
        question3(pk[0], pk[1], 2)
        print("M2")
        question3(pk[1], pk[2], 3)
        
    elif selected =='4':
        #generate public keys
        question1(g,p,sks)
        #get digital signature of sk1
        hash_msg, generated_r, generated_s, y = generate_signature(generate_message(pk[0], pk[1], amnt[1]), p, q, g, sk1)
        #verify digital signature of sk1
        verify_signature(hash_msg, generated_r , generated_s, g, p, q, y)
        #get digital signature of sk2
        hash_msg, generated_r, generated_s, y = generate_signature(generate_message(pk[1], pk[2], amnt[2]), p, q, g, sk2)

    elif selected == '5':
        find_nounce()

selector()
    
