class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, key):
        temp = self.head
        if temp is not None:
            if temp.data == key:
                self.head = temp.next
                temp = None
                return
        while temp is not None:
            if temp.data == key:
                break
            prev = temp
            temp = temp.next
        if temp == None:
            return
        prev.next = temp.next
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

# Создание односвязного списка
sll = SinglyLinkedList()
sll.append(1)
sll.append(2)
sll.append(3)
sll.prepend(0)
print(sll.display())  # Вывод: [0, 1, 2, 3]

sll.delete(2)
print(sll.display())  # Вывод: [0, 1, 3]

print(sll.search(1))  # Вывод: True
print(sll.search(2))  # Вывод: False

print(sll.get(2))  # Вывод: 3
