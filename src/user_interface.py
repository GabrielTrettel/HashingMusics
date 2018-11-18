#!/usr/bin/python3
import sys
from engine import Builder


def parseInput(args):
    template = [('-s',str,None), ('-m',str,None), ('-l',float,1)]#, ('-t',str,False)]
    template_help = {'-s': 'por um sentimento que existe na base de dados',
                     '-m': 'por uma musica (entre aspas simples caso tiver espaços)',
                     '-l': 'por um numero de zero a um representando a quão proximo deseja a busca'
                     }#'-t': 'pelos os limites inferiores e superiores, separados por vírgula, da playlist'}

    args_parse = dict()
    
    for item,type_converter,default in template:
        args_parse[item] = default
        for i,arg in enumerate(args[1:]):
            if arg == item:
                try:
                    if len(args[i+2]) == 2 and args[i+2][0] == '-': raise ValueError
                    args_parse[item] = type_converter(args[i+2])
                except:
                    print(f"INPUT ERROR:\no indicador '{item}' precisa ser seguido {template_help[item]}")
                    return False
                break

    return args_parse



if __name__ == '__main__':
    engine = Builder()

    args = sys.argv
    
    if len(args) == 1:
        print(engine.getMusics())
    elif args[1] == '--metadados':
        engine.printInfos()

    entries = parseInput(args) 
    
    if entries:
        print(engine.searchDB(entries))

    # print for debug purposes
    #print('\n'.join([f'{k}  -  {v}' for k,v in args_parse.items()]))
