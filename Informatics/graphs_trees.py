class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value):
        if value <= self.value:
            if self.left is None:
                self.left = TreeNode(value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = TreeNode(value)
            else:
                self.right.insert(value)

    def to_list(self):
        left = self.left.to_list() if self.left else None
        right = self.right.to_list() if self.right else None
        return [self.value, left, right]


def build_binary_tree(values):
    if not values:
        return []

    root = TreeNode(values[0])
    for value in values[1:]:
        root.insert(value)

    return root.to_list()


# Пример использования
values = eval(input())
print(build_binary_tree(values))
