import heapq

def max_tasks():
    n, a = map(int, input().split())
    tasks = []
    for _ in range(n):
        x, y = map(int, input().split())
        tasks.append((x, y))

    tasks.sort()  # Сортируем по минимальному требуемому умению

    heap = []
    count = 0
    i = 0

    while i < n or heap:
        while i < n and tasks[i][0] <= a:
            heapq.heappush(heap, -tasks[i][1])  # Добавляем в кучу с отрицанием для максимального прироста
            i += 1

        if not heap:
            break

        a += -heapq.heappop(heap)  # Увеличиваем умение Васи
        count += 1

    print(count)

max_tasks()
