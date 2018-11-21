#!/usr/bin/python3

import operator
import pickle
from tqdm import tqdm

B = 11
K = 2753
def multHash(value):
    return sum([ord(char)**(qtd+B) for qtd,char in enumerate(str(value))]) % K


def defaultHash(value=""):
    return hash(value) % 2753

def benchmark(words, funcao):
        tot = 0
        col = 0

        frequency = dict()
        for word in words:
            i = funcao(word)
            
            if i not in frequency:
                frequency[i] = 1
                tot += 1
            else:
                col += 1
                frequency[i] += 1

        sorted_x = sorted(frequency.items(), key=operator.itemgetter(1))

        print(f"min key: {min(list(frequency.keys()))}\nmax value: {max(list(frequency.values()))}")
        print(f"# keys: {len(frequency.keys())}")
        print(f'B = {B}\nK = {K}')
        print(f"qtd of words: {len(words)}")
        print(f"Média de colisões = {tot/col}")

        with open("saida"+f"{str(funcao)[:18]}.txt", 'w') as f:
            header = 'x,y\n'
            for item in sorted_x:
                header += f"{item[0]},{item[1]}\n"
            header += '\n\n\n'
            f.writelines(header)


if __name__ == '__main__':
    words = pickle.load(open('words.pkl', 'rb'))
    benchmark(words, multHash)
