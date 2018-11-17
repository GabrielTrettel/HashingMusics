#!/usr/bin/python3
from container import DictionaryHash, SetHash
from naive_bayes import NBClassifier
import sys
import pickle
import os

class Builder:

    def __init__(self):
        self.model_lyrics_path = sys.path[0][:-3] + "data_base/"
        self.new_lyrics_path   = ""

        self.DB_SEARCH         = DictionaryHash
        
        self.DB_SEARCH_FILE    = sys.path[0][:-3] + "search_DB.pkl"
        self.musics_folder     = "~/Musics"
       

    def buildWizard(self):

        welcome_header = """
            .  .         .               .   ,
            |  |         |   o           |\ /|         o
            |--| ,-: ,-. |-. . ;-. ,-:   | V | . . ,-. . ,-.
            |  | | | `-. | | | | | | |   |   | | | `-. | |
            '  ' `-` `-' ' ' ' ' ' `-|   '   ' `-` `-' ' `-'
                                   `-'
                         """
        print(welcome_header)
        print(self.model_lyrics_path)
        print("\nBem vindo ao assistente de configuração do seu ambiente.")
        
        self.new_lyrics_path = input("Onde você gostaria de configurar seu diretório de novas letras a serem classificadas?\n")

        musics_folder    = input(f"\nOnde voce gostaria de configurar a pasta onde os arquivos de audio estão? (por padrão: {self.musics_folder})\n") 
    
        if len(musics_folder) > 0:
            self.musics_folder = musics_folder

        q1 = input("Deseja classificar as musicas novas agora? (s/n)  ")
        if q1 == 's' or q1 == 'S' or q1 == 'Y' or q1 == 'y':
            self.buildSentimentMusicMap()

        

    def buildSentimentMusicMap(self):
        try:
            self.DB_SEARCH = picke.load(open('../search_DB.pkl', 'rb'))
        except:
            pass    
        
        train = [f"{self.model_lyrics_path}{file}" for file in os.listdir(self.model_lyrics_path)]
        print(train)
        classifier = NBClassifier(train)
        classifier.train()




if __name__ == '__main__':
    print(sys.path)
    instancia = Builder()
        
    instancia.buildWizard()
