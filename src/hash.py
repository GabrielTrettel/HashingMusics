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
    x = x[:max(0,len(x)-truncate)]
    x = x[max(0, len(x)-K):]

    return int(x, 2)


def benchmark():
        # 1239 palavras
        words = pickle.load(open('words.pkl', 'rb'))

        frequency = dict()
        for word in words:
            i = hash_multiplicacao(word)
            if i not in frequency:
                frequency[i] = 1
            else:
                frequency[i] += 1

        sorted_x = sorted(frequency.items(), key=operator.itemgetter(1))

        print("min key: ", min(list(frequency.keys())))

        print('x,y')
        for item in sorted_x:
            print(f"{item[0]},{item[1]}")


# if __name__ == '__main__':
