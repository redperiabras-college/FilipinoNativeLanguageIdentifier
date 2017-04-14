import os
from nltk.corpus import wordnet

file = open(os.path.join('data\\processed', 'cebuano.txt'))
temp = file.read().split()

words = []

for word in temp:
    if not wordnet.synsets(word):
        words.append(word)
    else:
        print(word)

file.close()

file = open(os.path.join('data\\processed', 'cebuano.txt'), 'w')

for word in words:
    file.write(word + "\n")

file.close()