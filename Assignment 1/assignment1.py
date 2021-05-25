import numpy
import matplotlib.pyplot as plt

f = open('ciphertext.txt', 'r')
ciphertext = f.read()
f.close()


def frequency(cipher):
    frequencydict = {}
    for text in cipher:
        if text in frequencydict:
            frequencydict[text] += 1
        else:
            frequencydict[text] =  1
        
    for i in frequencydict:
        print(i, frequencydict[i])
    plot(frequencydict)

def plot(frequencydict):
    letters = sorted(list(frequencydict.keys()))
    frequency = []
    for letter in letters:
        frequency.append(frequencydict[letter])
    print(letters)

    plt.bar(letters,frequency)
    plt.title('Letters VS Frequency')
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.show()


# part 2A:
def chunk(cipher, n):

    dictionarylist = []

    for x in range(n):
        dictionarylist.append({})

    chunks = [cipher[i:i+n] for i in range(0, len(cipher),n)]
    for chunk in chunks:     
        for x in range(len(chunk)):  
            if chunk[x] in dictionarylist[x]:
                dictionarylist[x][chunk[x]] += 1
            else:
                dictionarylist[x][chunk[x]] = 1
    #frequencydict.items()

    for i in dictionarylist:
        print(i)
    plot_first_chunk(chunks[0], cipher)

    #print("FIRST 6", frequencydict['agpygm'])
    #plot(frequencydict)

# part 2B
def plot_first_chunk(chunk, cipher):
    frequencydict = {}
    for letter in cipher:
        if letter in chunk:
            if letter in frequencydict:
                frequencydict[letter] += 1
            else:
                frequencydict[letter] = 1
    for i in frequencydict:
        print(i, frequencydict[i])
    #plot(frequencydict)

    letters = sorted(list(frequencydict.keys()))
    frequency = []
    for letter in chunk:
        frequency.append(get_freq_percentage(letter, frequencydict, len(cipher)))
        print(letter, get_freq_percentage(letter, frequencydict, len(cipher)))

    plt.bar(letters,frequency)
    plt.title('Letters VS Frequency')
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.show()


#question 3
def get_freq_percentage(letter, frequencydict, cipherlength):
    return (frequencydict[letter] / cipherlength) * 100


chunk(ciphertext, 6)


""" frequencydict = {}
dictionarylist = []
for x in range(n):
    dictionarylist.append({})

for chunk in chunks:
    for x in range(n):
        dictionarylist[x][chunk[x]] += 1 

  1 2 3 4 5 6
a 4 6 3
b 3 5 2
c
d """




# chunk the text by length
# return list of chunks


#frequency(ciphertext)

