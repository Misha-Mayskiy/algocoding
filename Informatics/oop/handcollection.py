class HandCollection:
    def __init__(self, key_type, v_type):
        self.data = []
        self.sort_key = []
        self.size = 0
        self.key_type = key_type
        self.v_type = v_type

    def add(self, key, value):
        if not isinstance(key, self.key_type) or not isinstance(value, self.v_type):
            raise TypeError("Error: key or value type mismatch")

        for i in range(len(self.sort_key)):
            if self.sort_key[i][0] == key:
                raise ValueError("Error: duplicate keys")
            if self.sort_key[i][0] > key:
                self.sort_key.insert(i, (key, self.size))
                break
        else:
            self.sort_key.append((key, self.size))

        self.data.append((key, value))
        self.size += 1

    def delete(self, key):
        left, right = 0, len(self.sort_key)
        while right - left > 1:
            mid = (left + right) // 2
            if self.sort_key[mid][0] <= key:
                left = mid
            else:
                right = mid

        if self.sort_key[left][0] != key:
            raise KeyError("Error: key not found")

        index_to_remove = self.sort_key[left][1]
        self.data[index_to_remove] = (None, None)
        del self.sort_key[left]

    def get(self, index):
        if index < 0 or index >= len(self.data):
            raise IndexError("Error: index out of range")
        key, value = self.data[index]
        if key is None:
            raise ValueError("Error: item at this index has been removed")
        return value

    def find(self, key):
        l, r = 0, len(self.sort_key)
        while r - l > 1:
            mid = (l + r) // 2
            if self.sort_key[mid][0] <= key:
                l = mid
            else:
                r = mid

        if self.sort_key[l][0] != key:
            return None

        i = self.sort_key[l][1]
        return self.data[i][1]


d = HandCollection(int, str)
d.add(1, "one")
d.add(2, "two")
d.add(3, "three")
print(str(d.find(2) == "two").lower())
