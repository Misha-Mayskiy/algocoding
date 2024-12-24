class TreeNode:
    def __init__(self, key1, key2, value):
        self.key1 = key1
        self.key2 = key2
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.core = None

    def add(self, key, value):
        if self.core is None:
            self.core = TreeNode(key, None, value)
        else:
            self._add(self.core, key, value)

    def _add(self, node, key, value):
        if key < node.key1:
            if node.left is None:
                node.left = TreeNode(key, None, value)
            else:
                self._add(node.left, key, value)
        else:
            if node.right is None:
                node.right = TreeNode(key, None, value)
            else:
                self._add(node.right, key, value)

    def search(self, key):
        return self._search(self.core, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key1:
            return node.value
        elif key < node.key1:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

class TwoKeyBinaryTree:
    def __init__(self):
        self.tree1 = BinaryTree()
        self.tree2 = BinaryTree()

    def add(self, key1, key2, value):
        self.tree1.add(key1, (key2, value))
        self.tree2.add(key2, (key1, value))

    def search(self, key1, key2=None):
        if key2 is None:
            return self.tree1.search(key1)
        else:
            result1 = self.tree1.search(key1)
            if result1 is None:
                return None
            result2 = self.tree2.search(key2)
            if result2 is None:
                return None
            return result1[1] if result1[0] == key2 else None


'''Предположим, что у нас есть данные о студентах, 
где 1 ключ - это идентификатор студента,
а 2 ключ - это номер курса, который студент проходит. 
Мы можем хранить и искать информацию о студентах 
как по идентификатору студента, так и по номеру курса.'''
tree = TwoKeyBinaryTree()
tree.add(1, 101, "Alice")
tree.add(2, 102, "Bob")
tree.add(3, 103, "Charlie")
tree.add(4, 101, "David")

# Поиск по одному ключу (идентификатор студента)
print('true' if tree.search(1) is not None else 'false')
# print(tree.search(2) is not None)
# print(tree.search(5) is not None)

# Поиск по двум ключам (идентификатор студента и номер курса)
# print(tree.search(1, 101) is not None)  # Вывод: true
# print(tree.search(4, 101) is not None)  # Вывод: true
# print(tree.search(3, 102) is not None)  # Вывод: false
