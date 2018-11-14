#!/usr/bin/python3
import sys

welcome_header = """
    .  .         .               .   ,
    |  |         |   o           |\ /|         o
    |--| ,-: ,-. |-. . ;-. ,-:   | V | . . ,-. . ,-.
    |  | | | `-. | | | | | | |   |   | | | `-. | |
    '  ' `-` `-' ' ' ' ' ' `-|   '   ' `-` `-' ' `-'
                           `-'
                 """

$ programa --metadados                                      <- retorna os metadados das musicas/sentimentos
$ programa --help                                           <- mostra a janela de ajuda

$ programa -s "amor"                                  <- abre a lista de musicas num editor
$ programa -b "happy"                                      <- busca uma musica em toda a lista de musicas

$ programa -s "sentimento" -b "musica"                      <- busca casamento perfeito de musica no sentimento
$ programa -b "musica"     -l int([0, 1])

$ programa -s "sentimento" -b "musica" -l int([0, 1])       <- retorna musicas parecidas com o nome "musica" (caro)
$ programa -s "sentimento" -t threshold int(low) int(up)    <-   ||    uma lista de tamanho up-low



if __name__ == '__main__':
    print(sys.argv)
    args = sys.argv

    if len(args) <= 2:
        if args[1] == "--metadados":
            print('metadados')
            # printMetadados()
        elif args[1] == '--help':
            print('--help')
            # printHelp()

    elif len(args) <= 3:
        if args == '-s':
            print("buscando -s")
            searchMusic(sentiment=argsv[2])
        elif args[1] == '-b':
            print("buscando -b")
            # searchMusic(music=args[2])
        else:
            raise ValueError('input invalido')

    elif len(args) <= 4:
