def gnome_sort(arr, n):
    index = 0
    while index < n:
        if index == 0:
            index += 1
        if arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1


import random
arr = list(range(999999))
random.shuffle(arr)
random.shuffle(arr)
print(arr)
gnome_sort(arr, len(arr))
print(arr)
