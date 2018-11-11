#!/usr/bin/python3
import pickle
# h(x) = (x.c div 2(b – k)/2) mod 2k
def hash_multiplicacao(value):
    K = 10
    B = 16
    C = bin(32)[2:]
    truncate = int(((B - K) / 2))

    x = bin(sum([ord(char) for char in value]))[2:]
    x = (max(0, 16-len(x)) * '0') + x
    x += C
    x = x[:max(0,len(x)-truncate)]
    x = x[max(0, len(x)-K):]

    return int(x, 2)


if __name__ == '__main__':

    # 1239 palavras
    words = pickle.load(open('words.pkl', 'rb'))

    frequency = dict()

    for word in words:
        i = hash_multiplicacao(word)
        if i not in frequency:
            frequency[i] = 1
        else:
            frequency[i] += 1


    import operator
    sorted_x = sorted(frequency.items(), key=operator.itemgetter(1))

    print('x,y')
    for item in sorted_x:
        print(f"{item[0]},{item[1]}")
