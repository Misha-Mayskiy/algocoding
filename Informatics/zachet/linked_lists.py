class SingleNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    # Добавление в начало
    def add_first(self, data):
        new_node = SingleNode(data)
        new_node.next = self.head
        self.head = new_node

    # Добавление в конец
    def add_last(self, data):
        new_node = SingleNode(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    # Удаление по значению
    def remove(self, data):
        if not self.head:
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
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
        return " -> ".join(result) + " -> None"


# Демонстрация операций
sll = SinglyLinkedList()
sll.add_first(3)  # [3]
sll.add_first(1)  # [1 -> 3]
sll.add_last(5)   # [1 -> 3 -> 5]
sll.add_last(7)   # [1 -> 3 -> 5 -> 7]
sll.remove(3)     # [1 -> 5 -> 7]
print("Односвязный список:", sll)
print("Поиск 5:", sll.search(5))  # True
print("Элемент с индексом 1:", sll.get_at(1))  # 5
