#!/usr/bin/python3
import sys
from engine import Builder
welcome_header = """
    .  .         .               .   ,
    |  |         |   o           |\ /|         o
    |--| ,-: ,-. |-. . ;-. ,-:   | V | . . ,-. . ,-.
    |  | | | `-. | | | | | | |   |   | | | `-. | |
    '  ' `-` `-' ' ' ' ' ' `-|   '   ' `-` `-' ' `-'
                           `-'
                 """

# $ programa --metadados                                      <- retorna os metadados das musicas/sentimentos
# $ programa --help                                           <- mostra a janela de ajuda
# 
# $ programa -s "amor"                                  <- abre a lista de musicas num editor
# $ programa -b "happy"                                      <- busca uma musica em toda a lista de musicas
# 
# $ programa -s "sentimento" -b "musica"                      <- busca casamento perfeito de musica no sentimento
# $ programa -b "musica"     -l int([0, 1])
# 
# $ programa -s "sentimento" -b "musica" -l int([0, 1])       <- retorna musicas parecidas com o nome "musica" (caro)
# 
# $ programa -s "sentimento" -t threshold low-up    <-   ||    uma lista de tamanho up-low




if __name__ == '__main__':
    engine = Builder()

    args = sys.argv
    template = [('-s',str,None), ('-m',str,None), ('-l',float,1)]#, ('-t',str,False)]
    template_help = {'-s': 'por um sentimento que existe na base de dados',
                     '-m': 'por uma musica (entre aspas simples caso tiver espaços)',
                     '-l': 'por um numero de zero a um representando a quão proximo deseja a busca'
                     }#'-t': 'pelos os limites inferiores e superiores, separados por vírgula, da playlist'}

    args_parse = dict()
    flag = False
    for item,type_converter,default in template:
        args_parse[item] = default
        for i,arg in enumerate(args[1:]):
            if arg == item:
                try:
                    if len(args[i+2]) == 2 and args[i+2][0] == '-': raise ValueError
                    args_parse[item] = type_converter(args[i+2])
                except:
                    print(f"INPUT ERROR:\no indicador '{item}' precisa ser seguido {template_help[item]}")
                    flag = True
                break

        if flag: break
    
    if not flag:
        engine.searchDB(args_parse)

    # print for debug purposes
    print('\n'.join([f'{k}  -  {v}' for k,v in args_parse.items()]))
