import os
from encodings.aliases import aliases
from LanguageModels import Markov

model_cebuano = Markov.MarkovChain(open(os.path.join('LanguageModels//data//processed', 'cebuano.txt'), encoding='utf8'),'Cebuano')
model_kapampangan = Markov.MarkovChain(open(os.path.join('LanguageModels//data//processed', 'kapampangan.txt'), encoding='utf8'),'Kapampangan')
model_pangasinan = Markov.MarkovChain(open(os.path.join('LanguageModels//data//processed', 'pangasinense.txt'), encoding='utf8'), 'Pangasinan')




models = []
models.append(model_cebuano)
models.append(model_kapampangan)
models.append(model_pangasinan)