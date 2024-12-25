class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class InverseBinaryTree:
    def __init__(self):
        self.root = None

    def add(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._add(self.root, value)

    def _add(self, node, value):
        if value < node.value:
            if node.left:
                self._add(node.left, value)
            else:
                node.left = Node(value)
        else:
            if node.right:
                self._add(node.right, value)
            else:
                node.right = Node(value)

    def find_deepest_and_largest(self):
        def traverse(node, depth):
            if not node:
                return None, depth, float('-inf')
            if not node.left and not node.right:
                return node, depth, node.value

            left_node, left_depth, left_max = traverse(node.left, depth + 1)
            right_node, right_depth, right_max = traverse(node.right, depth + 1)

            if left_depth > right_depth or (left_depth == right_depth and left_max > right_max):
                return left_node, left_depth, left_max
            else:
                return right_node, right_depth, right_max

        return traverse(self.root, 0)[0]

    def make_deepest_root(self):
        deepest_node = self.find_deepest_and_largest()

        def reassign(node, parent):
            if node == deepest_node:
                return None

            if parent and parent.left == node:
                parent.left = None
            elif parent and parent.right == node:
                parent.right = None

            return node

        def relocate(node, new_root):
            if not node:
                return
            if node != deepest_node:
                self.add(node.value)
            relocate(node.left, new_root)
            relocate(node.right, new_root)

        self.root = deepest_node
        relocate(reassign(self.root, None), self.root)

    def to_list(self):
        def node_to_list(node):
            if not node:
                return []
            return [node.value, node_to_list(node.left), node_to_list(node.right)]

        return node_to_list(self.root)


if __name__ == "__main__":
    values = list(map(int, input().split()))

    tree = InverseBinaryTree()
    for value in values:
        tree.add(value)

    tree.make_deepest_root()
    print(tree.to_list())
