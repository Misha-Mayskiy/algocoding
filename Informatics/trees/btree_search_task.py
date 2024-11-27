# class N:
#     def __init__(self, t, leaf=False):
#         self.t = t
#         self.k = []
#         self.c = []
#         self.leaf = leaf
#
#     def insert(self, v):
#         i = len(self.k) - 1
#         if self.leaf:
#             while i >= 0 and v < self.k[i]:
#                 i -= 1
#             self.k.insert(i + 1, v)
#         else:
#             while i >= 0 and v < self.k[i]:
#                 i -= 1
#             i += 1
#             if len(self.c[i].k) == 2 * self.t - 1:
#                 self.split(i)
#                 if v > self.k[i]:
#                     i += 1
#             self.c[i].insert(v)
#
#     def split(self, i):
#         t = self.t
#         n = self.c[i]
#         mid = n.k[t - 1]
#         new_node = N(t, leaf=n.leaf)
#         new_node.k = n.k[t:]
#         n.k = n.k[:t - 1]
#         if not n.leaf:
#             new_node.c = n.c[t:]
#             n.c = n.c[:t]
#         self.c.insert(i + 1, new_node)
#         self.k.insert(i, mid)
#
#     def search(self, low, high, res):
#         i = 0
#         while i < len(self.k) and self.k[i] < low:
#             i += 1
#         while i < len(self.k) and self.k[i] <= high:
#             res.append(self.k[i])
#             if not self.leaf:
#                 self.c[i].search(low, high, res)
#             i += 1
#         if not self.leaf and i < len(self.c):
#             self.c[i].search(low, high, res)
#
#
# class T:
#     def __init__(self, t):
#         self.t = t
#         self.root = N(t, leaf=True)
#
#     def add(self, v):
#         r = self.root
#         if len(r.k) == 2 * self.t - 1:
#             new_root = N(self.t)
#             new_root.c.append(r)
#             new_root.split(0)
#             self.root = new_root
#             self.root.insert(v)
#         else:
#             r.insert(v)
#
#     def find(self, low, high):
#         res = []
#         self.root.search(low, high, res)
#         return res
#
#
# nums = list(map(int, input().strip().split(',')))
# low, high = map(int, input().strip().split(','))
# t = 3
# tree = T(t)
# for n in nums:
#     tree.add(n)
# print(','.join(map(str, sorted(tree.find(low, high)))))

class Node:
    def __init__(self, key, row, col):
        self.key = key
        self.row = row
        self.col = col
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, row, col):
        if not self.root:
            self.root = Node(key, row, col)
        else:
            self._insert(self.root, key, row, col)

    def _insert(self, current, key, row, col):
        if key < current.key:
            if current.left:
                self._insert(current.left, key, row, col)
            else:
                current.left = Node(key, row, col)
        else:
            if current.right:
                self._insert(current.right, key, row, col)
            else:
                current.right = Node(key, row, col)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, current, key):
        if not current:
            return None
        if current.key == key:
            return current.row, current.col
        if key < current.key:
            return self._search(current.left, key)
        return self._search(current.right, key)

def main():
    import sys
    input = sys.stdin.read
    data = input().split('\n')

    matrix = [list(map(int, row.split())) for row in data[:-2]]
    target = int(data[-2])

    bst = BST()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            bst.insert(matrix[i][j], i, j)

    result = bst.search(target)
    if result:
        print(result[0], result[1])

main()
