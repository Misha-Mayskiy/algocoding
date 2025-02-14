class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def display(self):
        return self.items


# Создание стека
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(stack.display())  # Вывод: [1, 2, 3]

print(stack.pop())  # Вывод: 3
print(stack.display())  # Вывод: [1, 2]

print(stack.peek())  # Вывод: 2
print(stack.is_empty())  # Вывод: False
print(stack.size())  # Вывод: 2
