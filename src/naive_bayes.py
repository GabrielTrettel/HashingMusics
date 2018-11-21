#!/usr/bin/python3
from container import DictionaryHash, SetHash
import sys

try:
    from nltk.corpus import stopwords
except:
    print("Você precisa instalar uma biblioteca do python chamada nltk\nE rodar o seguinte comando num console:")
    print(">>> import nltk\n>>> nltk.download('stopwords')\n")
    sys.exit()


from nltk.stem import PorterStemmer
import os
import re
import math

regex = r"[-'a-zA-ZÀ-ÖØ-öø-ÿ]+"


class NBClassifier:
    def __init__(self, training_file=None):
        self.stop_words    = SetHash(stopwords.words('english'))           # Palavras que desconsideraremos por baixo valor semantico
        self.ps            = PorterStemmer()                               # Algoritmo de radicalização Porter
        self.table         = str.maketrans("","",".,:!@#$%*(){\}[]?;")     # retira caracteres indesejados

        self.n_musics      = 0                 # Guarda a quantidade de musicas
        self.sentiments    = DictionaryHash()  # Quantidade de ocorrencias para cada classe {c1:20, c4:30}
        self.V             = SetHash()         # Um conjunto com todas as palavras (vocabulario) {p1, p2, p3}
        self.bigdoc        = DictionaryHash()  # {classe1: [palavra1, palavra2,...], classe2:[p3, p1,...]}

        self.logprior      = DictionaryHash()  # prob a priori para cada classe {p1:0.4, p2:0.6}
        self.loglikelihood = DictionaryHash()  # log da afinidade de cada palavra para cada classe

        # self.sentiments    = dict()
        # self.V             = set()
        # self.bigdoc        = dict()
        # self.logprior      = dict()
        # self.loglikelihood = dict()

        if training_file is not None:
            self.load_data(training_file)


    def load_data(self, training_files):
        for file in training_files:
            with open(file,'r') as training_document:
                self.n_musics += 1

                lines = [line.strip('\n') for line in training_document.readlines()]
                music_sentiments = lines[0].split(',')
                
                lyric = lines[1:]

                for sentiment in music_sentiments:
                    if sentiment not in self.sentiments:
                        self.sentiments[sentiment] = 0
                        self.bigdoc[sentiment] = []
                    self.sentiments[sentiment] += 1

                for line in lyric:
                    for word in re.findall(regex, line):
                        word = word.lower().translate(self.table)
                        word = self.ps.stem(word)
                        if word not in self.stop_words:
                            self.V.add(word)
                            for sentiment in music_sentiments:
                                self.bigdoc[sentiment].append(word)

        print(f"Dados da base de dados de treino:\nsentimentos={len(self.sentiments)} \t musicas={self.n_musics} \t palavras={len(self.V)}\n")


    def train(self):
        for sentiment in self.sentiments.keys():
            Ndoc = self.n_musics
            Nc   = self.sentiments[sentiment]

            print("Definindo o que", sentiment, "significa")
            self.logprior[sentiment]  = math.log(Nc/Ndoc)

            count_wc = 0
            for word in self.V:
                count_wc += self.bigdoc[sentiment].count(word)

            for word in self.V:
                self.loglikelihood[(word,sentiment)] = math.log((self.bigdoc[sentiment].count(word) + 1)
                                                                / (1 + count_wc + len(self.V)))


    # Recebe com argumento um objeto arquivo.readlines() só com a letra da musica
    def predict(self, lyric):
        s = dict([])

        for sentiment in self.sentiments.keys():
            s[sentiment] = self.logprior[sentiment]
            for line in lyric:
                for word in re.findall(regex, line):
                    word = word.lower().translate(self.table)
                    word = self.ps.stem(word)

                    if word in self.V and word not in self.stop_words:
                        s[sentiment] += self.loglikelihood[(word,sentiment)]

        return max(s, key=s.get)



    def organiza_teste(self, files):
        y_pred = []
        y_true = []

        for file in files:
            with open(file,'r') as training_document:

                lines = [line.strip('\n') for line in training_document.readlines()]
                music_sentiments = lines[0].split(',')
                lyric = lines[1:]

                y_true.append(music_sentiments[0])
                y_pred.append(self.predict(lyric))
                

        iguais = [x for x in range(len(y_pred)) if (y_pred[x] == y_true[x])]
        print("%2.2f%% de acerto" % float((len(iguais)*100)/len(y_pred)))


if __name__ == '__main__':
    folder = sys.argv[1]
    inputs = os.listdir(folder)
    files = [folder+input for input in inputs]


    NBC = NBClassifier(files[14:])
    NBC.train()
     
    NBC.organiza_teste(files[:14])
