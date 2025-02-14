class DoubleNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    # Добавление в начало
    def add_first(self, data):
        new_node = DoubleNode(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    # Добавление в конец
    def add_last(self, data):
        new_node = DoubleNode(data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    # Удаление по значению
    def remove(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                return
            current = current.next

    # Поиск
    def search(self, data):
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    # Получение по индексу
    def get_at(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                return current.data
            count += 1
            current = current.next
        raise IndexError("Index out of range")

    # Вывод списка
    def __str__(self):
        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next
        return " <-> ".join(result) + " -> None"


# Демонстрация операций
dll = DoublyLinkedList()
dll.add_first(3)  # [3]
dll.add_first(1)  # [1 <-> 3]
dll.add_last(5)   # [1 <-> 3 <-> 5]
dll.add_last(7)   # [1 <-> 3 <-> 5 <-> 7]
dll.remove(3)     # [1 <-> 5 <-> 7]
print("\nДвусвязный список:", dll)
print("Поиск 7:", dll.search(7))  # True
print("Элемент с индексом 2:", dll.get_at(2))  # 7
