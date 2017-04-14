import re
from collections import OrderedDict

class input():
    def __init__(self, content):
        self.__n = 3  # trigram
        self.words = self.__tokenize(content)
        self.alphabet = self.__characters()
        self.ngrams = self.__model()

    def __tokenize(self, content):
        words = re.compile(r'\w(?:[-\w]*\w)?').findall(content)
        words = [x.lower() for x in words]
        words.sort()

        return words

    def __characters(self):
        alphabet = []
        for word in self.words:
            for i in range(len(word)):
                if word[i] not in alphabet:
                    alphabet.append(word[i])

        alphabet.sort()

        return alphabet

    def __model(self):

        bound = self.__n - 1
        ngrams = {}

        for word in self.words:
            if len(word) < self.__n:
                pass

            for i in range(len(word) - bound):
                key = () #generated ngram

                for j in range(bound):
                    key = key + (word[i+j],)

                if key in ngrams:
                    ngrams[key].append(word[i + bound])
                else:
                    ngrams[key] = [word[i + bound]]

        return OrderedDict(sorted(ngrams.items(), key=lambda t: t[0]))

    def countStartingWith(self, i):
        count = 1 #start with 1 for smoothing

        for word in self.words:
            if word[:1] is i:
                count += 1

        return count

    def countPairs(self, i, j):
        if i in self.ngrams.keys():
            count = 1 #start with 1 for smoothing
            for value in self.ngrams.get(i):
                if value is j:
                    count += 1
            return count
        else:
            return 1 #return for smoothing
