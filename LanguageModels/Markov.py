import os
import math
import re
from collections import OrderedDict

class MarkovChain(object):

    def __init__(self, open_file, id):
        self.id = id

        self.__openFile = open_file
        # the alphabet used in the traaining data
        self.alphabet = []
        #words in the training document
        self.k = self.__tokenize()
        self.__M = len(self.alphabet)
        #number of words in the training document
        self.__L = len(self.k)
        #length of each words
        #self.__t = {} - this can be easily obtained with len(self.__k[x])

        self.ngrams = {}
        self.ngramsCounts = {}
        self.__n = 3  # trigram for default
        self.__model()

    def __tokenize(self):
        self.__openFile.seek(0)
        data = self.__openFile.read()
        words = re.compile(r'\w(?:[-\w]*\w)?').findall(data)
        words = [x.lower() for x in words]
        words.sort()

        #get all characters involved
        for word in words:
            for i in range(len(word)):
                if word[i] not in self.alphabet:
                    self.alphabet.append(word[i])

        self.alphabet.sort()

        return words

    def __model(self):

        """
        Generates n-grams from the words given in training data.
        Creates the language __model
        :return:
        """

        for word in self.k:
            if len(word) < self.__n:
                pass

            bound = self.__n - 1
            for i in range(len(word) - bound):
                key = () #generated ngram

                for j in range(bound):
                    key = key + (word[i+j],)

                if key in self.ngrams:
                    self.ngrams[key].append(word[i + bound])
                    self.ngramsCounts[key] = self.ngramsCounts.get(key, 0) + 1  # count of the ngram
                else:
                    self.ngrams[key] = [word[i + bound]]
                    self.ngramsCounts[key] = 1

        self.ngrams = OrderedDict(sorted(self.ngrams.items(), key=lambda t: t[0]))

    # def generate_markov_text(self, size=25):
    #     seed = random.randint(0, self.word_size - 3)
    #     seed_word, next_word = self.words[seed], self.words[seed + 1]
    #     w1, w2 = seed_word, next_word
    #     gen_words = []
    #     for i in range(size):
    #         gen_words.append(w1)
    #         w1, w2 = w2, random.choice(self.cache[(w1, w2)])
    #     gen_words.append(w2)
    #     return ' '.join(gen_words)

    def init_prob(self, i):
        """
        Determines the initial probability of letter i
        :param i:
        :return initial probability:
        """

        #Determine the occurence of the ngram as first n letter
        count = 0  # start with 1 for smoothing
        for word in self.k:
            if word[:1] is i:
                count += 1

        #smoothing: laplace method for single distribution
        #reference: https://www.youtube.com/watch?v=gCI-ZC7irbY
        return count / (self.__L + count)

    def trans_prob(self, i, j):
        """
        Determine the transition probability from i to j
        :param i:
        :param j:
        :return:
        """

        #check inputs
        bound =  self.__n - 1

        if i in self.ngrams.keys():
            # Count the pairs
            xypairs = 0  # start with one for smoothing
            xzpairs = len(self.ngrams.get(i))

            for value in self.ngrams.get(i):
                for i in value:
                    if j == i:
                        xypairs += 1

            # smoothing: laplace method for conditional distribution
            # reference: https://www.youtube.com/watch?v=gCI-ZC7irbY
            # reference: https://www.youtube.com/watch?v=ebeGh8HM4Jo
            return xypairs / (xypairs + xzpairs)

        else:
            return 0

    def export(self,output):
        file = open(os.path.join('languagemodels\models', output+'.csv'),'w')
        line = ",init_prob,"

        #header
        for letter in self.alphabet:
            line += letter + ","

        file.write(line+"\n")

        for key, value in self.ngrams.items():
            line = "\""+ str(key) + "\"," + str(self.init_prob(key))
            for x in self.alphabet:
                line += ","+ str(self.trans_prob(key,x))
            file.write(line+"\n")

        file.close()

    def evaluateInput(self, model_input):
        #return value initialization
        value = 0
        init = [(model_input.countStartingWith(x) * math.log1p(self.init_prob(x)) ) for x in model_input.alphabet]

        trans = []
        for key, value in model_input.ngrams.items():
            pair = []

            for j in value:
                pair.append(model_input.countPairs(key, j) * math.log1p(self.trans_prob(key, j)))

            trans.append(sum(pair))

        sigma_ni = sum(init)
        sigma_nij = sum(trans)
        value = sigma_ni + sigma_nij

        print("\nNumber of Words: ", len(model_input.words))
        print("Model:",self.id)
        print("Inits:",sigma_ni)
        print("Pairs:",sigma_nij)
        print(self.id, "Evaluation:",value)
        return value