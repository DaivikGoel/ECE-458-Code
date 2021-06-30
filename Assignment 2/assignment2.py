

p = 168199388701209853920129085113302407023173962717160229197318545484823101018386724351964316301278642143567435810448472465887143222934545154943005714265124445244247988777471773193847131514083030740407543233616696550197643519458134465700691569680905568000063025830089599260400096259430726498683087138415465107499

sks = [432398415306986194693973996870836079581453988813,165849943586922055423650237226339279137759546603,627658512551971075308886219669315148725310346887 ]

g = 94389192776327398589845326980349814526433869093412782345430946059206568804005181600855825906142967271872548375877738949875812540433223444968461350789461385043775029963900638123183435133537262152973355498432995364505138912569755859623649866375135353179362670798771770711847430626954864269888988371113567502852

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
    import hashlib
    
    
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

selector()
    

