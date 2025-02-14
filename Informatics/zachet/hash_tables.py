class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])

    def get(self, key):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None

    def delete(self, key):
        index = self._hash(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                return True
        return False

    def display(self):
        return self.table

# Пример использования хеш-таблицы
hash_table = HashTable()
hash_table.insert("apple", 1)
hash_table.insert("banana", 2)
hash_table.insert("orange", 3)

print(hash_table.get("apple"))  # Вывод: 1
print(hash_table.get("banana"))  # Вывод: 2
print(hash_table.get("orange"))  # Вывод: 3

hash_table.delete("banana")
print(hash_table.get("banana"))  # Вывод: None

print(hash_table.display())  # Вывод: [[['apple', 1]], [['orange', 3]], [], [], [], [], [], [], [], []]
