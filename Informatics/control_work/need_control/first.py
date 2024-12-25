class MergeSorter:
    def __init__(self, data):
        self.data = data

    def sort(self):
        return self._merge_sort(self.data)

    def _merge_sort(self, array):
        if len(array) <= 1:
            return array

        mid = len(array) // 2
        left = self._merge_sort(array[:mid])
        right = self._merge_sort(array[mid:])

        return self._merge(left, right)

    def _merge(self, left, right):
        sorts = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] > right[j]:
                sorts.append(left[i])
                i += 1
            else:
                sorts.append(right[j])
                j += 1

        sorts.extend(left[i:])
        sorts.extend(right[j:])

        return sorts


if __name__ == "__main__":
    inp = list(map(int, input().split(',')))
    sorter = MergeSorter(inp)
    print(sorter.sort())
