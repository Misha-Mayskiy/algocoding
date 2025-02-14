class Color:
    RED = True
    BLACK = False

class RBNode:
    def __init__(self, key, color=Color.RED):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(None, Color.BLACK)  # Виртуальные "листья"
        self.root = self.NIL

    # ------------------- Вспомогательные методы -------------------
    def _rotate_left(self, x):
        """Левый поворот вокруг узла x."""
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        """Правый поворот вокруг узла x."""
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _fix_insert(self, z):
        """Балансировка после вставки."""
        while z.parent and z.parent.color == Color.RED:
            if z.parent == z.parent.parent.left:
                uncle = z.parent.parent.right
                if uncle.color == Color.RED:
                    # Случай 1: Дядя красный → перекрашивание
                    z.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    # Случай 2: Дядя черный → поворот
                    if z == z.parent.right:
                        z = z.parent
                        self._rotate_left(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._rotate_right(z.parent.parent)
            else:
                # Симметричный случай для правого поддерева
                uncle = z.parent.parent.left
                if uncle.color == Color.RED:
                    z.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._rotate_right(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._rotate_left(z.parent.parent)
            if z == self.root:
                break
        self.root.color = Color.BLACK

    # ------------------- Основные операции -------------------
    def insert(self, key):
        """Вставка элемента."""
        z = RBNode(key)
        z.left = self.NIL
        z.right = self.NIL
        y = None
        x = self.root
        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        self._fix_insert(z)

    def _transplant(self, u, v):
        """Замена поддерева u на поддерево v."""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _fix_delete(self, x):
        """Балансировка после удаления."""
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == Color.RED:
                    # Случай 1: Брат красный → перекрасить и повернуть
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._rotate_left(x.parent)
                    s = x.parent.right
                if s.left.color == Color.BLACK and s.right.color == Color.BLACK:
                    # Случай 2: Оба ребенка брата черные
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.right.color == Color.BLACK:
                        # Случай 3: Правый ребенок брата черный
                        s.left.color = Color.BLACK
                        s.color = Color.RED
                        self._rotate_right(s)
                        s = x.parent.right
                    # Случай 4: Левый ребенок брата красный
                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.right.color = Color.BLACK
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                # Симметричный случай для правого поддерева
                s = x.parent.left
                if s.color == Color.RED:
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._rotate_right(x.parent)
                    s = x.parent.left
                if s.right.color == Color.BLACK and s.left.color == Color.BLACK:
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.left.color == Color.BLACK:
                        s.right.color = Color.BLACK
                        s.color = Color.RED
                        self._rotate_left(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.left.color = Color.BLACK
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = Color.BLACK

    def delete(self, key):
        """Удаление элемента."""
        z = self.root
        while z != self.NIL:
            if z.key == key:
                break
            elif key < z.key:
                z = z.left
            else:
                z = z.right
        if z == self.NIL:
            return  # Элемент не найден

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == Color.BLACK:
            self._fix_delete(x)

    def _minimum(self, node):
        """Находит минимальный узел в поддереве."""
        while node.left != self.NIL:
            node = node.left
        return node

    # ------------------- Поиск и вывод -------------------
    def search(self, key):
        """Поиск элемента."""
        current = self.root
        while current != self.NIL:
            if current.key == key:
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return False

    def _print_tree(self, node, indent="", last=True):
        """Визуализация дерева (для отладки)."""
        if node != self.NIL:
            print(indent, end="")
            if last:
                print("└── ", end="")
                indent += "    "
            else:
                print("├── ", end="")
                indent += "│   "
            color = "R" if node.color == Color.RED else "B"
            print(f"{node.key}({color})")
            self._print_tree(node.left, indent, False)
            self._print_tree(node.right, indent, True)

    def print_tree(self):
        """Вывод дерева на экран."""
        self._print_tree(self.root)

# Демонстрация операций
rbt = RedBlackTree()
print("Вставка элементов 10, 20, 30, 15, 25:")
rbt.insert(10)
rbt.print_tree()
rbt.insert(20)
rbt.print_tree()
rbt.insert(30)
rbt.print_tree()
rbt.insert(15)
rbt.print_tree()
rbt.insert(25)
rbt.print_tree()

print("\nУдаление элемента 20:")
rbt.delete(20)
rbt.print_tree()

print("\nПоиск элемента 25:", rbt.search(25))  # True
print("Поиск элемента 20:", rbt.search(20))  # False