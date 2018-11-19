#!/usr/bin/python3
import sys
from engine import Builder


template_help = {'-s': '-s \t precisa ser seguido por por um sentimento que existe na base de dados',
                 '-m': '-m \t precisa ser seguido por uma musica (entre aspas simples caso tiver espaços)',
                 '-l': '-l \t precisa ser seguido por um numero de zero a um representando a quão próximo deseja a busca',
                 '-p': '-p \t precisa ser seguidopor um aplicativo que reproduz música. Recomendamos o mplayer'}

help_msg = """
Uso: naivesearch [opção] [argumento] 
 ou: naivesearch [assistentes]

[opções]
As opçoes precisam estar em pares com seus argumentos. Multiplas opções são permitidas e
podem estar em qualquer ordem.

-s              Retorna da base de dados todas as músicas presentes com o sentimento indicado
                como argumento.
                
-m              Busca (casamento perfeito) a música indicada como argumento. Se a opção -s for
                utilizada junto com o -m, então a busca será para este sentimento, caso contrário
                a busca será feita para todos os sentimentos.

-l              Define um grau de liberdede para busca de músicas com -m. Precisa ser seguido por um 
                numero de 0-1 representando a quão proximo deseja procurar; 1=casamento perfeito,
                0.1 = seleciona musicas com o nome 10% parecido com o argumento

-p              Indica um reprodutor de música que tentará combinar o resultado da busca com os
                arquivos de áudio configurados na criação do banco de dados.
                (recomendados: mplayer e vlc)


[assistentes]
--musicas       Imprime na tela todas as musicas no banco de dados (cuidado, esta operação pode demorar)

--sentimentos   Imprime na tela todos os sentimentos no banco de dados

--metadados     Imprime algumas informações sobre o banco de dados com as musicas

--delete        Deleta o banco de dados utilizado para fazer a busca

--help          Imprime esta ajuda

--remake        Refaz as configurações já definidas e abre a central que pode criar novamente o banco 
                de dados caso novas musicas sejam inseridas dentro do diretório de classificação
                
                """

def parseInput(args):
    template = [('-s',str,None), ('-m',str,None), ('-l',float,1), ('-p',str,None)]

    args_parse = dict()
    
    for item,type_converter,default in template:
        args_parse[item] = default
        for i,arg in enumerate(args[1:]):
            if arg == item:
                try:
                    if len(args[i+2]) == 2 and args[i+2][0] == '-': raise ValueError
                    args_parse[item] = type_converter(args[i+2])
                    args.pop(i+2)
                    args.remove(arg)
                except:
                    print(f"INPUT ERROR:\n{template_help[item]}")
                    return False
                break
    
    if len(args) > 1:
        print("Argumentos inválidos. --help para ajuda")
        return False

    return args_parse



if __name__ == '__main__':
    engine = Builder()
    status = engine.openDB()
    args = sys.argv

        
    if len(args) == 1 or args[1] == '--help':
        print(help_msg)
    
    elif not status and args[1] != '--make':
        print("Você não possui o banco de dados para pesquisa. --make para construir")
    
    elif args[1] == '--make':
        engine.buildWizard()

    elif args[1] == '--musicas':
        print(engine.getMusics())

    elif args[1] == '--sentimentos':
        print(engine.getSentiments())

    elif args[1] == '--metadados':
        engine.printInfos()
    
    elif args[1] == '--remake' and status:
        engine.buildWizard()
    
    elif args[1] == '--delete':
        engine.deleteDB()

    elif status:
        entries = parseInput(args)   
        if entries:
            engine.searchDB(entries)

    
