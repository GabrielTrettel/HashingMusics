#!/usr/bin/python3
from hash import multHash

class Hash:
    def __init__(self):
        self._table = [[] for x in range(1024)]
        self._length = 0


    def __hash__(self, attrib):
        return multHash(str(attrib))

    def __iter__(self, key=True, value=True):
        for item in self._table:
            for element in item:
                yield element


    def __len__(self):
        return self._length


    def __contains__(self, key):
        index = self.__hash__(key)
        if len(self._table[index]) <= 0: return False

        if isinstance(self._table[index][0], list):
            equals = lambda a,b: a[0] == b
        else:
            equals = lambda a,b: a == b

        for item in self._table[index]:
            if equals(item, key):
                return True
        return False


    def pop(self, key):
        index = self.__hash__(key)
        if len(self._table[index]) <= 0: return False

        if isinstance(self._table[index][0], list):
            equals = lambda a,b: a[0] == b
        else:
            equals = lambda a,b: a == b

        for i,item in enumerate(self._table[index]):
            if equals(item, key):
                del self._table[index][i]
                self._length -= 1
                return item
        return None



class DictionaryHash(Hash):
    def __init__(self):
        super(DictionaryHash, self).__init__ ()


    def __setitem__(self, key, value):
        index = self.__hash__(key)
        is_in_table = False
        for item in self._table[index]:
            if item[0] == key:
                item[1] = value
                is_in_table = True
                break
        if not is_in_table:
            self._table[index].append([key,value])
            self._length += 1


    def __getitem__(self, key):
        index = self.__hash__(key)
        for item in self._table[index]:
            if item[0] == key:
                return item[1]
        return None


    def __delitem__(self, key):
        index = self.__hash__(key)

        for i,item in enumerate(self._table[index]):
            if item[0] == key:
                del self._table[index][i]
                self._length -= 1
                return True
        return False


    def __str__(self):
        string = "{"
        for item in self._table:
            if len(item) > 0:
                string += ", ".join(f'{it[0]}:{it[1]}' for it in item) + ',\n'
        return string.strip(', ') + '}'


    def keys(self):
        for item in self._table:
            if len(item) > 0:
                for element in item:
                    yield element[0]


    def values(self):
        for item in self._table:
            if len(item) > 0:
                for element in item:
                    yield element[1]



class SetHash(Hash):
    def __init__(self):
        super(SetHash, self).__init__ ()

    def __str__(self):
        string = "{"
        for item in self._table:
            if len(item) > 0:
                string += ", ".join(str(elemment) for elemment in item) + ", "
        return string.strip(', ') + "}"


    def add(self, key):
        index = self.__hash__(key)
        is_in_table = False
        for item in self._table[index]:
            if item == key:
                is_in_table = True
                break
        if not is_in_table:
            self._table[index].append(key)
            self._length += 1


    def remove(self, key):
        index = self.__hash__(key)
        for i,item in enumerate(self._table[index]):
            if item == key:
                del self._table[index][i]
                self._length -= 1
                return True
        return False
