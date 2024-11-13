class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_right(self, y):
        print(f"Right rotation on {y.key}")
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x):
        print(f"Left rotation on {x.key}")
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    def insert(self, node, key):
        if not node:
            return Node(key)
        elif key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        self.update_height(node)
        balance = self.get_balance(node)

        # Левое смещение
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)
        # Правое смещение
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)
        # Левый-Правый случай
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        # Правый-Левый случай
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def display(self, node, prefix="", is_left=True):
        if node:
            connector = "├── " if is_left else "└── "
            print(prefix + connector + str(node.key))
            child_prefix = prefix + ("│   " if is_left else "    ")
            if node.left or node.right:
                if node.left:
                    self.display(node.left, child_prefix, True)
                else:
                    print(child_prefix + "├── None")
                if node.right:
                    self.display(node.right, child_prefix, False)
                else:
                    print(child_prefix + "└── None")


# Создание дерева и вставка узлов
tree = AVLTree()
root = None

keys = [20, 4, 15]
for key in keys:
    print(f"\nВставка {key}:")
    root = tree.insert(root, key)
    tree.display(root)
