class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y):
        x, T2 = y.left, y.left.right
        x.right, y.left = y, T2
        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x):
        y, T2 = x.right, x.right.left
        y.left, x.right = x, T2
        self.update_height(x)
        self.update_height(y)
        return y

    def insert(self, node, key):
        if not node:
            return Node(key)
        if key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        self.update_height(node)
        balance = self.get_balance(node)

        # Балансировка
        if balance > 1:
            return self.rotate_right(node) if key < node.left.key else self.rotate_right(self.rotate_left(node.left))
        if balance < -1:
            return self.rotate_left(node) if key > node.right.key else self.rotate_left(self.rotate_right(node.right))
        return node

    def display(self, node, prefix="", is_left=True):
        if node:
            connector = "├── " if is_left else "└── "
            print(prefix + connector + str(node.key))
            child_prefix = prefix + ("│   " if is_left else "    ")
            if node.left or node.right:
                self.display(node.left, child_prefix, True) if node.left else print(child_prefix + "├── None")
                self.display(node.right, child_prefix, False) if node.right else print(child_prefix + "└── None")

# Пример использования AVL-дерева
tree = AVLTree()
root = None

# Пример с поворотами
keys = [20, 4, 15]
for key in keys:
    print(f"\nВставка {key}:")
    root = tree.insert(root, key)
    tree.display(root)
