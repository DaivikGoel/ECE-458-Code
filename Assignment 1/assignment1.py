import numpy
import matplotlib.pyplot as plt

f = open('ciphertext.txt', 'r')
ciphertext = f.read()
f.close()

# Question 1
def frequency(cipher):
    # we use a dictionary to measure the amount of times the lettes are in the cipher
    frequencydict = {}
    for text in cipher:
        if text in frequencydict:
            frequencydict[text] += 1
        else:
            frequencydict[text] =  1
    #print out the letters and their frequency
    print("FREQUENCY OF EACH LETTER IN THE CIPHER: ")
    for i in frequencydict:
        print(i, frequencydict[i])
    plot(frequencydict)

#method to plot frequency of each character
def plot(frequencydict):
    letters = sorted(list(frequencydict.keys()))
    frequency = []
    for letter in letters:
        frequency.append(frequencydict[letter])
    #prints a bar plot
    plt.bar(letters,frequency)
    plt.title('Letters VS Frequency')
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.show()


# part 2A:
def chunk(cipher, n):
    #list of dictionaries for letters of each position. 
    dictionarylist = []

    for x in range(n):
        dictionarylist.append({})

    #splits ciphertext into chunks of length n each
    chunks = [cipher[i:i+n] for i in range(0, len(cipher),n)]
    for chunk in chunks:     
        #update freq of char appearence in dictionary at each position relative to chunk
        for x in range(len(chunk)):  
            if chunk[x] in dictionarylist[x]:
                dictionarylist[x][chunk[x]] += 1
            else:
                dictionarylist[x][chunk[x]] = 1
    print("CHUNKS: " , chunks)
    return chunks, dictionarylist


# part 2B
def plot_first_chunk(chunk, cipher):
    #plots the frequency percentage of the first chunk
    frequencydict = {}
    for letter in cipher:
        #finds the frequency of letters in the first chunk in the cipher and adds to dictionary
        if letter in chunk:
            if letter in frequencydict:
                frequencydict[letter] += 1
            else:
                frequencydict[letter] = 1
    print("FREQUENCY OF EACH LETTER IN THE FIRST CHUNK IN THE CIPHER: ")
    for i in frequencydict:
        print(i, frequencydict[i])

    letters = sorted(list(frequencydict.keys()))
    frequency = []
    for letter in letters:
        #gets percentages of letters relative to the cipher
        frequency.append(get_freq_percentage(letter, frequencydict, len(cipher)))
    #make a bar graph of letters
    plt.bar(letters,frequency)
    plt.title('Letters VS Frequency Percentage')
    plt.xlabel('Letters')
    plt.ylabel('Frequency Percentage')
    plt.show()


def get_freq_percentage(letter, frequencydict, cipherlength):
    #create a percentage
    return int((frequencydict[letter] / cipherlength) * 100)

#question 3
def get_secret_key(dictionarylist):
    shift = []
    #e is the most common letter in the dictionary. We take the most common letter at each positon and assume it to be e. We try finding the shift amount accordingly
    position = 0
    for i in dictionarylist:
        i = sorted(i.items(), key=lambda tup: tup[1], reverse=True)
        #Adding shift amount of each position to an array
        shift.append(ord(i[0][0]) - ord('e') )
        position += 1
        print("POSITION ", position, " FREQUENCY ANALYSIS: ",i)
        print(shift)

    secretkey = ''
    for lettershift in shift:
        #using the shift amount to get the secret key. 
        if lettershift > 0:
            #the secret key is the position of each letter relative to a
            secretkey += chr(lettershift + 97)
        else:
            #this is for the wrap around case ie. a - 2 = y 
            secretkey += chr(26 + lettershift + 97)  
    print("SECRET KEY:" , secretkey)
    return secretkey, shift

#question 4
def decrypttext(shift, chunks):
    #after knowing the shift we can find out the plain text
    plaintext =''
    for chunk in chunks:
        for x in range(len(chunk)):
            #we take for each chunk and shift according to what we found the shift to be
            charno = ord(chunk[x]) - shift[x]
            #covering various cases like wrap around
            if charno > 122: 
                plaintext += chr((charno - 123)+ 97)
            elif charno > 96:
                plaintext += chr(charno)
            else: 
                plaintext += chr(charno + 26)
    print("PLAIN TEXT:" , plaintext)



def question1(cipher): 
    frequency(cipher)

def question2and3(cipher, n):
    chunks, dictionarylist = chunk(cipher, 6)
    secretkey, shift = get_secret_key(dictionarylist)
    decrypttext(shift, chunks)
    plot_first_chunk(chunks[0], cipher)

# choose which question you want to do
#question1(ciphertext)
question2and3(ciphertext, 6)