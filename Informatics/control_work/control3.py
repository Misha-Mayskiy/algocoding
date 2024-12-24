# 1 task
# from random import choice
#
#
# def quicksort(nums):
#     if len(nums) <= 1:
#         return nums
#     else:
#         q = choice(nums)
#     l_nums = [n for n in nums if n < q]
#
#     e_nums = [q] * nums.count(q)
#     b_nums = [n for n in nums if n > q]
#     return quicksort(l_nums) + e_nums + quicksort(b_nums)
#
# chars = list(input())
# print(''.join(quicksort(chars)))

# 2 task
# def pyramid_sort(a):
#     n = len(a)
#     for i in range(n // 2 - 1, -1, -1):
#         heapify(a, n, i)
#     for i in range(n - 1, 0, -1):
#         a[0], a[i] = a[i], a[0]
#         heapify(a, i, 0)
#
# def heapify(a, n, i):
#     m = i
#     l = 2 * i + 1
#     r = 2 * i + 2
#     if l < n and a[l] > a[m]:
#         m = l
#     if r < n and a[r] > a[m]:
#         m = r
#     if m != i:
#         a[i], a[m] = a[m], a[i]
#         heapify(a, n, m)
#
# lst = [int(x) for x in input().strip().split(',')]
# pyramid_sort(lst)
# print(','.join(map(str, lst)))

# 3 task
# def tim_sort(data, key_func=lambda x: x):
#     def insertion_sort(subarray, left, right):
#         for i in range(left + 1, right + 1):
#             pos = i
#             while pos > left and key_func(subarray[pos]) < key_func(subarray[pos - 1]):
#                 subarray[pos], subarray[pos - 1] = subarray[pos - 1], subarray[pos]
#                 pos -= 1
#
#     def merge_sort(m, left_p, seredina, right_p):
#         left_half = m[left_p:seredina + 1]
#         right_half = m[seredina + 1:right_p + 1]
#         i, j, k = 0, 0, left_p
#         while i < len(left_half) and j < len(right_half):
#             if key_func(left_half[i]) <= key_func(right_half[j]):
#                 m[k] = left_half[i]
#                 i += 1
#             else:
#                 m[k] = right_half[j]
#                 j += 1
#             k += 1
#         while i < len(left_half):
#             m[k] = left_half[i]
#             i += 1
#             k += 1
#         while j < len(right_half):
#             m[k] = right_half[j]
#             j += 1
#             k += 1
#
#     n = len(data)
#     minimum = 32
#     for i in range(0, n, minimum):
#         end_p = min(i + minimum - 1, n - 1)
#         insertion_sort(data, i, end_p)
#     a = minimum
#     while a < n:
#         for i in range(0, n, 2 * a):
#             seredina = min(n - 1, i + a - 1)
#             end_p = min(i + 2 * a - 1, n - 1)
#
#             if seredina < end_p:
#                 merge_sort(data, i, seredina, end_p)
#         a *= 2
#
#
# m = eval(input())
# tim_sort(m, key_func=lambda pair: pair[1])
# print("[" + ",".join(f"({a},{b})" for a, b in m) + "]")

# 4 task
# import sys
#
#
# def find_path(graph, start, end):
#     n = len(graph)
#     q = [start]
#     roditel = [-1] * n
#     roditel[start] = start
#
#     while q:
#         now = q.pop(0)  # Извлекаем первый элемент
#         if now == end:
#             break
#         for sosed in range(n):
#             if roditel[sosed] == -1 and graph[now][sosed] > 0:
#                 roditel[sosed] = now
#                 q.append(sosed)
#
#     path = []
#     if roditel[end] != -1:
#         node = end
#         while node != start:
#             path.append((roditel[node], node))
#             node = roditel[node]
#         path.reverse()
#
#     return path
#
#
# def min_cut(graph, start, end):
#     ans = 0
#     while True:
#         path = find_path(graph, start, end)
#         if not path:
#             break
#         minim = min(graph[u][v] for u, v in path)
#         ans += minim
#         for u, v in path:
#             graph[u][v] -= minim
#             graph[v][u] += minim
#     return ans
#
#
# graph = []
# for line in sys.stdin.readlines():
#     line = line.strip()
#     if line:
#         graph.append(list(map(int, line.split())))
# start, end = graph.pop(-1)
# print(min_cut(graph, start - 1, end - 1))

# 5 task
class Node:
    def __init__(self):
        self.child = {}
        self.is_end = False

class Tree:
    def __init__(self):
        self.root = Node()

    def add(self, word):
        n = self.root
        for i in word:
            if i not in n.child:
                n.child[i] = Node()
            n = n.child[i]
        n.is_end = True

    def find(self, lenn):
        res = []
        self._collect(self.root, "", lenn, res)
        return res

    def _collect(self, node, prefix, lenn, res):
        if node.is_end and len(prefix) == lenn:
            res.append(prefix)
        for i, child in node.child.items():
            self._collect(child, prefix + i, lenn, res)

def clean(text):
    return text.translate({ord(ch): None for ch in ".,!?;:\"'()[]{}-"}).lower().split()

def search_words(text, length):
    words = clean(text)
    trie = Tree()
    for word in words:
        trie.add(word)
    return trie.find(length)

text = input()
length = int(input())
result = search_words(text, length)
print(" ".join(result))
