#!/usr/bin/python3
from container import DictionaryHash, SetHash
from naive_bayes import NBClassifier
import Levenshtein as LEV
import sys
import pickle
import os

class Builder:

    def __init__(self):
        self.model_lyrics_path = sys.path[0][:-3] + "data_base/"
        self.new_lyrics_path   = sys.path[0][:-3] + "to_predict_db/"
        self.DB_SEARCH_FILE    = sys.path[0][:-3] + "search_DB.pkl"
        self.musics_folder     = "~/Musics"
        
        self.DB_SEARCH         = DictionaryHash()
        self.__openDB()
        

        
    def __openDB(self):
        try:
            self.DB_SEARCH = pickle.load(open(self.DB_SEARCH_FILE, 'rb'))
        except:
            print("Você não possui o banco de dados para pesquisa. Deseja iniciar o")
            print("assistente de configuração agora? (s/n)  ", end="")
            i = input()

            if i.lower() == 's' or i.lower() == 'y':
                self.buildWizard()


    def buildWizard(self):
        os.system('clear')
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
        
        print("Onde você gostaria de configurar seu diretório de novas letras a serem classificadas?")
        new_lyrics_path = input(f"(por padrão: {self.new_lyrics_path}) ")

        if len(new_lyrics_path) > 0:
            self.new_lyrics_path = new_lyrics_path

        print("\nOnde voce gostaria de configurar a pasta onde os arquivos de audio estão?")
        musics_folder = input(f"por padrão: {self.musics_folder})   ") 
    
        if len(musics_folder) > 0:
            self.musics_folder = musics_folder

        q1 = input("\nDeseja classificar as musicas novas agora? (s/n)  ")
        if q1.lower() == 's' or q1.lower() == 'y':
            self.buildSentimentMusicMap()

        

    def buildSentimentMusicMap(self):
        try:
            self.DB_SEARCH = pickle.load(open(self.DB_SEARCH_FILE, 'rb'))
        except:
            pass 

        os.system('clear')
        train = [f"{self.model_lyrics_path}{file}" for file in os.listdir(self.model_lyrics_path)]
        classifier = NBClassifier(train)
        
        print('────────────────────────────────────────────────────────────────────────────\n')
        classifier.train()
        
        files_to_predict = [f'{self.new_lyrics_path}{file}' for file in os.listdir(self.new_lyrics_path)] 
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
        
        pickle.dump(self.DB_SEARCH, open(self.DB_SEARCH_FILE, 'wb'))
        
    def deleteDB(self):
        try:
            os.system(f'rm {self.DB_SEARCH_FILE}')
        except:
            print("Não foi possivel deleter o banco de dados. Provavelmente o\narquivo não existe ou está em outro lugar")
    


    def getClasses(self):
        return "\n".join(self.DB_SEARCH.keys())



    def getMusics(self):
        return "\n".join(self.DB_SEARCH.values())



    def __equal(self, m1, m2, ratio):
        if m2 == None: return True
        if ratio == 1:
            return m1 == m2
        else:
            return LEV.ratio(m1, m2) >= ratio

    def searchDB(self, inputs):
        sentiments = ""

        if inputs['-s'] != None:
            if inputs['-s'] in self.DB_SEARCH:
                sentiments = [inputs['-s']]
            else:
                print(f"Sentimento não encontrado na base de dados.\n Tente algum desses:\n{', '.join(self.DB_SEARCH.keys())}")
                return False
        else:
            sentiments = self.DB_SEARCH.keys()
        
        m_s = inputs['-m']
        ratio = inputs['-l']
        musics = []
        for sentiment in sentiments:
            musics.extend(m for m in self.DB_SEARCH[sentiment] if self.__equal(m, m_s, ratio))
        
        
        songs = "\n".join(musics)

        with open('/tmp/PLAYLIST.txt', 'w') as f:
            f.writelines(songs)
     
        os.system('$EDITOR /tmp/PLAYLIST.txt')
        with open ('/tmp/PLAYLIST.txt', 'r') as f:
            musics = [m.strip('\n') for m in f.readlines()]

        return musics

if __name__ == '__main__':
    instancia = Builder()
    #instancia.deleteDB()
