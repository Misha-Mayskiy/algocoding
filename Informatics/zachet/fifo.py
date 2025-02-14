class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def display(self):
        return self.items


# Создание очереди
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print(queue.display())  # Вывод: [1, 2, 3]

print(queue.dequeue())  # Вывод: 1
print(queue.display())  # Вывод: [2, 3]

print(queue.front())  # Вывод: 2
print(queue.is_empty())  # Вывод: False
print(queue.size())  # Вывод: 2
