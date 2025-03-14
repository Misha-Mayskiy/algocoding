import matplotlib.pyplot as plt
import numpy as np
import random

# Обновляем карту с обозначениями и доработкой деталей

fig, ax = plt.subplots(figsize=(12, 12))

# Фон карты (суша)
ax.set_facecolor('#e0dabd')

# Море и океаны
water_color = '#5d9cec'
ax.fill_between([-1, 11], -1, 3, color=water_color, label="Море Норн")
ax.fill_between([-1, 3], 3, 6, color=water_color, label="Западное море")

# Озёра
lake_positions = [(6, 7, 1), (8, 5, 0.8)]
for x, y, r in lake_positions:
    circle = plt.Circle((x, y), r, color=water_color, ec="black", label="Озеро" if x == 6 else "")
    ax.add_patch(circle)

# Река Вальдис
river_x = [5, 5.5, 6, 6.2, 6.5, 6.8, 7]
river_y = [10, 9, 8, 7, 6, 5, 4]
ax.plot(river_x, river_y, color=water_color, linewidth=3, label="Река Вальдис")

# Горы Айронкрест (северо-восток)
for _ in range(8):
    x, y = random.uniform(7, 10), random.uniform(7, 10)
    ax.scatter(x, y, marker="^", color="gray", s=100, label="Горы" if _ == 0 else "")

# Пустыня Орим (юг)
for _ in range(50):
    x, y = random.uniform(4, 8), random.uniform(0, 3)
    ax.scatter(x, y, marker=".", color="sandybrown", alpha=0.6, label="Пустыня" if _ == 0 else "")

# Лес Тенарис (север)
for _ in range(50):
    x, y = random.uniform(2, 6), random.uniform(7, 10)
    ax.scatter(x, y, marker="*", color="darkgreen", s=50, label="Лес" if _ == 0 else "")

# Степи Сольвейг (запад)
for _ in range(50):
    x, y = random.uniform(0, 3), random.uniform(4, 8)
    ax.scatter(x, y, marker=".", color="yellowgreen", alpha=0.5, label="Степи" if _ == 0 else "")

# Полуостров Кассия (восток)
ax.fill_between([7, 10], 2, 4, color='#e0dabd', label="Полуостров Кассия")

# Острова Мист (юго-запад)
island_positions = [(1, 1), (1.5, 1.5), (2, 0.5)]
for x, y in island_positions:
    circle = plt.Circle((x, y), 0.3, color='#e0dabd', ec="black", label="Острова" if x == 1 else "")
    ax.add_patch(circle)

# Автономии и этнические зоны
ax.scatter(4, 7, color="purple", s=100, label="Автономия Дракенхольм", marker="s")
ax.scatter(3, 5, color="orange", s=100, label="Зона диаспор Лисмир", marker="s")

# Экономически важные зоны
ax.scatter(6, 3, color="black", s=100, label="Шахты Карнас", marker="X")
ax.scatter(7, 6, color="brown", s=100, label="Плодородные земли Иллион", marker="o")
ax.scatter(3, 3, color="blue", s=100, label="Торговый порт Вестгард", marker="D")
ax.scatter(6, 5, color="red", s=100, label="Город-государство Арктон", marker="P")

# Политическая столица
ax.scatter(5, 5, color="gold", s=200, label="Столица Аурелии", marker="*")

# Добавление границ соседних государств
ax.plot([-1, 11], [10, 10], color="black", linestyle="--", label="Граница с Бореалией")
ax.plot([0, 0], [0, 10], color="black", linestyle="--", label="Граница с Альтанией")
ax.plot([10, 10], [0, 10], color="black", linestyle="--", label="Граница с Зелестией")

# Подписи географических объектов
labels = {
    (5, 1): "Пустыня Орим",
    (5, 9): "Река Вальдис",
    (7, 8): "Горы Айронкрест",
    (6, 6): "Озеро Луминос",
    (8, 5): "Озеро Сапфир",
    (3, 8): "Лес Тенарис",
    (1, 6): "Степи Сольвейг",
    (9, 3): "Полуостров Кассия",
    (1, 2): "Острова Мист",
    (4, 7): "Автономия Дракенхольм",
    (3, 5): "Зона диаспор Лисмир",
    (6, 3): "Шахты Карнас",
    (7, 6): "Плодородные земли Иллион",
    (3, 3): "Торговый порт Вестгард",
    (6, 5): "Город-государство Арктон",
    (5, 5): "Аурелия (столица)",
}

for (x, y), name in labels.items():
    ax.text(x, y, name, fontsize=9, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))

# Названия соседних государств
ax.text(5, 10.5, "БОреалия", fontsize=12, ha='center', va='center', fontweight='bold', color='black')
ax.text(-0.5, 5, "Альтания", fontsize=12, ha='center', va='center', fontweight='bold', rotation=90, color='black')
ax.text(10.5, 5, "Зелестия", fontsize=12, ha='center', va='center', fontweight='bold', rotation=-90, color='black')

# Убираем оси
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 11)

# Легенда карты
ax.legend(loc="upper right", fontsize=8, frameon=True, facecolor="white")

# Показываем карту
plt.title("Карта государства Аурелия (с детализацией)")
plt.show()
