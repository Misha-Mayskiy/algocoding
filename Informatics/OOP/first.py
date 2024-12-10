import sys


class Node:
    """Класс для узла односвязного списка."""
    def __init__(self, value):
        self.value = value
        self.next = None


class CustomList:
    """Класс для односвязного списка чисел."""
    def __init__(self):
        self.head = None

    def add(self, value):
        """Добавляет элемент в конец списка."""
        new_node = Node(value)
        if not self.head:  # Если список пуст
            self.head = new_node
        else:
            current = self.head
            while current.next:  # Проходим до конца списка
                current = current.next
            current.next = new_node  # Присоединяем новый узел

    def remove(self, value):
        """Удаляет элемент из списка по значению."""
        current = self.head
        prev = None
        while current:
            if current.value == value:
                if prev:  # Если это не первый элемент
                    prev.next = current.next
                else:  # Если удаляем первый элемент
                    self.head = current.next
                return True  # Удаление успешно
            prev = current
            current = current.next
        return False  # Элемент не найден

    def __str__(self):
        """Возвращает строковое представление списка."""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.value))
            current = current.next
        return " -> ".join(elements)


def main():
    custom_list = CustomList()
    for line in sys.stdin:
        try:
            number = int(line.strip())
            custom_list.add(number)
        except ValueError:
            pass

    print(custom_list)


if __name__ == "__main__":
    main()
