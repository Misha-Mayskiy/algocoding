def min_lanterns_needed(N, A, X, B, Y): 
    # Если радиусы освещения X или Y равны 0, то эти фонари освещают только один дом 
    if X == 0: 
        X = 1 
    if Y == 0: 
        Y = 1 

    # Массив для отслеживания, освещён ли каждый дом 
    street = [False] * N 

    # Функция для установки фонарей 
    def place_lanterns(start, radius, count): 
        placed = 0 
        i = start 
        while i < N and placed < count: 
            if not street[i]: 
                # Покрываем все дома, которые находятся в радиусе освещения 
                for j in range(max(0, i - radius), min(N, i + radius + 1)): 
                    street[j] = True 
                placed += 1 
            i += (2 * radius + 1) 
        return placed 

    # Сначала расставляем фонари типа с большим радиусом 
    if X > Y: 
        A = place_lanterns(0, X, A) 
        B = place_lanterns(0, Y, B) 
    else: 
        B = place_lanterns(0, Y, B) 
        A = place_lanterns(0, X, A) 

    # Проверяем, покрыты ли все дома 
    if all(street): 
        return A + B 
    else: 
        return -1  # Если не удалось покрыть все дома 

# Пример использования 
N = int(input()) 
A = int(input()) 
X = int(input()) 
B = int(input()) 
Y = int(input()) 

result = min_lanterns_needed(N, A, X, B, Y) 
print(result)