# class DataType:
#     pass
#
# class LRU:
#     def __init__(self, capacity, data_type):
#         self.count_contain = capacity
#         self.data_type = data_type
#         self.items = []
#         self.us_ord = []
#
#     def add(self, item):
#         if not isinstance(item, self.data_type):
#             return False
#
#         if len(self.items) < self.count_contain:
#             self.items.append(item)
#             self.us_ord.append(item)
#             return 'true'
#         else:
#             lru_item = self.us_ord.pop(0)
#             self.items.remove(lru_item)
#             self.items.append(item)
#             self.us_ord.append(item)
#             return 'true'
#
#     def get(self, index):
#         if 0 <= index < len(self.items):
#             item = self.items[index]
#             self.us_ord.remove(item)
#             self.us_ord.append(item)
#             return item
#         else:
#             return None
#
# # Пример использования
# class SubDataType(DataType):
#     pass
#
# lru = LRU(3, DataType)
#
# item = SubDataType()
#
# print(lru.add(item))

class DataType:
    pass

class LRU:
    def __init__(self, capacity, data_type):
        self.capacity = capacity
        self.data_type = data_type
        self.items = []
        self.usage_count = {}

    def add(self, item):
        if not isinstance(item, self.data_type):
            return None

        if len(self.items) < self.capacity:
            self.items.append(item)
            self.usage_count[item] = 0
            return 'true'
        else:
            lru_item = min(self.usage_count, key=self.usage_count.get)
            self.items.remove(lru_item)
            del self.usage_count[lru_item]
            self.items.append(item)
            self.usage_count[item] = 0
            return lru_item

    def get(self, index):
        if 0 <= index < len(self.items):
            item = self.items[index]
            self.usage_count[item] += 1
            return item
        else:
            return None


class SubDataType(DataType):
    pass

lru = LRU(3, DataType)

item1 = SubDataType()
item2 = SubDataType()
item3 = SubDataType()
item4 = SubDataType()

lru.add(item1)
lru.add(item2)
lru.add(item3)
replaced_item = lru.add(item4)  # item1 (наименее используемый элемент)

if replaced_item == item1:
    print('true')
