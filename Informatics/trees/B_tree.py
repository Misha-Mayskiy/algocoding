class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Минимальная степень (порядок) дерева
        self.leaf = leaf  # Лист ли это
        self.keys = []  # Ключи узла
        self.children = []  # Дети узла (для не листовых узлов)

    # Поиск ключа в поддереве с корнем в данном узле
    def find_key(self, key):
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1
        return idx

    # Вставка нового ключа в поддерево, где данный узел является корнем
    def insert_non_full(self, key):
        i = len(self.keys) - 1

        if self.leaf:
            self.keys.append(0)
            while i >= 0 and self.keys[i] > key:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and self.keys[i] > key:
                i -= 1
            if len(self.children[i + 1].keys) == 2 * self.t - 1:
                self.split_child(i + 1, self.children[i + 1])
                if self.keys[i + 1] < key:
                    i += 1
            self.children[i + 1].insert_non_full(key)

    # Разбиение дочернего узла при переполнении
    def split_child(self, i, y):
        z = BTreeNode(y.text, y.leaf)
        z.keys = y.keys[self.t:(2 * self.t - 1)]
        y.keys = y.keys[0:(self.t - 1)]

        if not y.leaf:
            z.children = y.child[self.t:(2 * self.t)]
            y.child = y.child[0:self.t]

        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys[self.t - 1])
        y.keys = y.keys[:self.t - 1]

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    # Поиск ключа начиная с корня
    def search(self, key, node=None):
        node = node if node else self.root
        i = node.find_key(key)

        if i < len(node.keys) and node.keys[i] == key:
            return node, i

        if node.leaf:
            return None

        return self.search(key, node.children[i])

    # Вставка ключа в дерево
    def insert(self, key):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, False)
            new_root.children.append(self.root)
            new_root.split_child(0, self.root)
            self.root = new_root
        self.root.insert_non_full(key)

    # Простое отображение дерева
    def display(self, node=None, level=0):
        node = node if node else self.root
        print("Level", level, ":", node.keys)
        if not node.leaf:
            for child in node.children:
                self.display(child, level + 1)

# Пример использования B-дерева
t = 3  # Порядок дерева
tree = BTree(t)

# Вставка ключей
for key in [10, 20, 5, 6, 12, 30, 7, 17]:
    tree.insert(key)

# Вывод B-дерева
print("B-Tree структура:")
tree.display()

# Поиск ключа
key_to_find = 6
found_node = tree.search(key_to_find)
print(f"\nПоиск ключа {key_to_find}: {'Найден' if found_node else 'Не найден'}")
