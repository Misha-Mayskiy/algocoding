def bin_search(sort_arr, need_find):
    left, right = 0, len(sort_arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if sort_arr[mid][0] == need_find:
            return sort_arr[mid][1]
        elif sort_arr[mid][0] < need_find:
            left = mid + 1
        else:
            right = mid - 1
    return -1


arr = list(map(int, input().split(",")))
elem = int(input())

ind_arr = list(zip(arr, range(len(arr))))
ind_arr.sort(key=lambda x: x[0])

ind_elem = bin_search(ind_arr, elem)
print(ind_elem) if ind_elem + 1 else print("Элемент не найден")
