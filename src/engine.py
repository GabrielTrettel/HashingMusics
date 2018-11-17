#!/usr/bin/python3
from container import DictionaryHash, SetHash
from naive_bayes import NBClassifier
import sys
import pickle
import os

class Builder:

    def __init__(self):
        self.model_lyrics_path = sys.path[0][:-3] + "data_base/"
        self.new_lyrics_path   = "/home/trettel/Documents/projects/HashingMusics/to_predict_db/"

        self.DB_SEARCH         = self.__openDB()
        
        self.DB_SEARCH_FILE    = sys.path[0][:-3] + "search_DB.pkl"
        self.musics_folder     = "~/Musics"
       

    def __openDB(self):
        try:
            return pickle.load(open(self.DB_SEARCH_FILE, 'rb'))
        except:
            return DictionaryHash()

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
        print("\nBem vindo ao assistente de configuração do seu ambiente.\n")
        
        new_lyrics_path = input(f"Onde você gostaria de configurar seu diretório de novas letras a serem classificadas?\n(por padrão: {self.new_lyrics_path}) ")
        if len(new_lyrics_path) > 0:
            self.new_lyrics_path = new_lyrics_path

        musics_folder    = input(f"\nOnde voce gostaria de configurar a pasta onde os arquivos de audio estão? (por padrão: {self.musics_folder})\n") 
    
        if len(musics_folder) > 0:
            self.musics_folder = musics_folder

        q1 = input("Deseja classificar as musicas novas agora? (s/n)  ")
        if q1 == 's' or q1 == 'S' or q1 == 'Y' or q1 == 'y':
            self.buildSentimentMusicMap()

        

    def buildSentimentMusicMap(self):
        try:
            self.DB_SEARCH = pickle.load(open('../search_DB.pkl', 'rb'))
        except:
            pass 

        print('\n\ṇ̣────────────────────────────────────────────────────────────────────────────────────────────────')
        train = [f"{self.model_lyrics_path}{file}" for file in os.listdir(self.model_lyrics_path)]
        classifier = NBClassifier(train)
        classifier.train()
        
        files_to_predict = [f"{self.new_lyrics_path}{file}" for file in os.listdir(self.new_lyrics_path)] 
        print()# print just a blank line 
        for file in  files_to_predict:
            with open(file, 'r') as f:
                sentiment = classifier.predict(f.readlines())
                print(sentiment, '\t-\t', file.split('/')[-1])
                
                form_file = file.split('/')[-1].strip(' ').lower()
                if str(sentiment) not in self.DB_SEARCH:
                    self.DB_SEARCH[sentiment] = SetHash()
                    self.DB_SEARCH[sentiment].add(form_file)
                else:                
                    self.DB_SEARCH[sentiment].add(form_file)
        print("\n")
        #print(self.DB_SEARCH)

if __name__ == '__main__':
    instancia = Builder()
    instancia.buildWizard()
