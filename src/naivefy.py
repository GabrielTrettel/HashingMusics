#!/usr/bin/python3
import sys
from engine import Builder


template_help = {'-s': '-s \t precisa ser seguido por por um sentimento que existe na base de dados',
                 '-m': '-m \t precisa ser seguido por uma música (entre aspas simples caso tiver espaços)',
                 '-l': '-l \t precisa ser seguido por um número de zero a um representando a quão próximo deseja a busca',
                 '-p': '-p \t precisa ser seguido por um aplicativo que reproduz música. Recomendamos o mplayer'}



help_msg = """

Uso: naivefy [opção] [argumento]
 ou: naivefy [assistentes]

As playlists criadas ficam salvas nesse diretório num arquivo chamado PLAYLIST.txt

[opções]
As opções precisam estar em pares com seus argumentos. Múltiplas opções são permitidas e
podem estar em qualquer ordem.

-s              Retorna da base de dados todas as músicas presentes com o sentimento indicado
                como argumento.
                
-m              Busca (casamento perfeito) a música indicada como argumento. Se a opção -s for
                utilizada junto com o -m, então a busca será para este sentimento, caso contrário
                a busca será feita para todos os sentimentos.

-l              Define um grau de liberdade para busca de músicas com -m. Precisa ser seguido por um
                número de 0-1 representando a quão próximo deseja procurar; 1=casamento perfeito,
                0.1 = seleciona músicas com o nome 10% parecido com o argumento

-p              Indica um reprodutor de música que tentará combinar o resultado da busca com os
                arquivos de áudio configurados na criação do banco de dados.
                (recomendados: mplayer e vlc)


[assistentes]
--músicas       Imprime na tela todas as músicas no banco de dados (cuidado, esta operação pode demorar)

--sentimentos   Imprime na tela todos os sentimentos no banco de dados

--metadados     Imprime algumas informações sobre o banco de dados com as músicas

--delete        Deleta o banco de dados utilizado para fazer a busca

--help          Imprime esta ajuda

--make          Abre um tutorial guiado de como configurar e montar o banco de dados

--remake        Refaz as configurações já definidas e abre a central que pode criar novamente o banco
                de dados caso novas músicas sejam inseridas dentro do diretório de classificação
                
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
    open_db = engine.openDB()
    args = sys.argv

        
    if len(args) == 1 or '--help' in args:
        print(help_msg)
    
    elif not open_db and '--make' not in args:
        print("Você não possui o banco de dados para pesquisa. --make para construir")
    
    elif '--make' in args:
        engine.buildWizard()

    elif '--musicas' in args:
        print(engine.getMusics())

    elif '--sentimentos' in args:
        print(engine.getSentiments())

    elif '--metadados' in args:
        engine.printInfos()
    
    elif '--remake' in args and open_db:
        engine.buildWizard()
    
    elif '--delete' in args: 
        engine.deleteDB()

    elif open_db:
        entries = parseInput(args)   
        if entries:
            engine.searchDB(entries)

    
