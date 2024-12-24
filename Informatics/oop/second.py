import sys


class CustomQueue:
    """Самосортирующаяся очередь чисел."""

    def __init__(self, sorter=None):
        """
        Инициализация очереди.
        :param sorter: Функция сортировки, по умолчанию сортирует по возрастанию.
        """
        self.queue = []
        self.sorter = sorter if sorter else lambda x: sorted(x)

    def add(self, value):
        """Добавляет элемент в очередь и сортирует её."""
        self.queue.append(value)
        self.queue = self.sorter(self.queue)

    def remove(self):
        """Удаляет первый элемент из очереди (FIFO)."""
        if self.queue:
            return self.queue.pop(0)
        return None

    def __str__(self):
        """Возвращает строковое представление очереди."""
        return " -> ".join(map(str, self.queue))


сustom_list = CustomQueue()
for line in sys.stdin:
    try:
        number = int(line.strip())
        сustom_list.add(number)
    except ValueError:
        pass

print(сustom_list)
