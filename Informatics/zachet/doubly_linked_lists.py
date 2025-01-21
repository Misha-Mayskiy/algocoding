class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = DoublyNode(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last

    def prepend(self, data):
        new_node = DoublyNode(data)
        new_node.next = self.head
        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node

    def delete(self, key):
        temp = self.head
        if temp is not None:
            if temp.data == key:
                self.head = temp.next
                self.head.prev = None
                temp = None
                return
        while temp is not None:
            if temp.data == key:
                break
            temp = temp.next
        if temp is None:
            return
        if temp.next is not None:
            temp.next.prev = temp.prev
        if temp.prev is not None:
            temp.prev.next = temp.next
        temp = None

    def search(self, key):
        current = self.head
        while current is not None:
            if current.data == key:
                return True
            current = current.next
        return False

    def get(self, index):
        current = self.head
        count = 0
        while current:
            if count == index:
                return current.data
            count += 1
            current = current.next
        return None

    def display(self):
        elems = []
        curr_node = self.head
        while curr_node:
            elems.append(curr_node.data)
            curr_node = curr_node.next
        return elems

# Создание многосвязного списка
dll = DoublyLinkedList()
dll.append(1)
dll.append(2)
dll.append(3)
dll.prepend(0)
print(dll.display())  # Вывод: [0, 1, 2, 3]

dll.delete(2)
print(dll.display())  # Вывод: [0, 1, 3]

print(dll.search(1))  # Вывод: True
print(dll.search(2))  # Вывод: False

print(dll.get(2))  # Вывод: 3
