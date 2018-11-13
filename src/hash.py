#!/usr/bin/python3

import operator
import pickle
# h(x) = (x*x div 2(b – k)/2) mod 2k
def multHash(value=""):
    K = 10
    B = 17
    truncate = int(((B - K) / 2))

    x = bin(sum([ord(char) for char in value]))[2:]
    x *= 2
    x = x[ :max(0,len(x)-truncate)]
    x = x[max(0, len(x)-K): ]

    return int(x, 2)

def defaultHash(value=""):
    return hash(value) % 1025


def benchmark(funcao):
        # 1239 palavras
        words = pickle.load(open('words.pkl', 'rb'))
        print(len(words))
        frequency = dict()
        for word in words:
            i = funcao(word)
            if i not in frequency:
                frequency[i] = 1
            else:
                frequency[i] += 1

        sorted_x = sorted(frequency.items(), key=operator.itemgetter(1))

        print(f"min key: {min(list(frequency.keys()))}\nmax value: {max(list(frequency.values()))} ")

        with open("saida"+f"{str(funcao)[:18]}.txt", 'w') as f:
            header = 'x,y\n'
            for item in sorted_x:
                header += f"{item[0]},{item[1]}\n"
            header += '\n\n\n'
            f.writelines(header)


if __name__ == '__main__':
    # benchmark(defaultHash)
    benchmark(multHash)
