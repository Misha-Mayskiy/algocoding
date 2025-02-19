import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Создаём фигуру и ось
fig, ax = plt.subplots(figsize=(12, 10))

# --- Наружные государства (слева и справа от Аурелии) ---
# Государство Альтания (слева)
state_left = patches.Rectangle((-40, 0), 40, 100, facecolor='lavender', edgecolor='black', alpha=0.5)
ax.add_patch(state_left)
ax.text(-20, 50, "Государство Альтания", fontsize=12, rotation=90, va='center', ha='center', color='black')

# Государство Зелестия (справа)
state_right = patches.Rectangle((100, 0), 40, 100, facecolor='lightcyan', edgecolor='black', alpha=0.5)
ax.add_patch(state_right)
ax.text(120, 50, "Государство Зелестия", fontsize=12, rotation=-90, va='center', ha='center', color='black')

# --- Основная территория государства "Аурелия" ---
country = patches.Rectangle((0, 0), 100, 100, linewidth=2, edgecolor='black', facecolor='lightgrey')
ax.add_patch(country)

# --- Внешние элементы: море, побережье ---
# Море (внешние области)
sea_bottom = patches.Rectangle((-50, -25), 250, 25, facecolor='skyblue', alpha=0.4)
sea_left   = patches.Rectangle((-50, -25), 50, 150, facecolor='skyblue', alpha=0.4)
ax.add_patch(sea_bottom)
ax.add_patch(sea_left)

# Побережье (южняя и западная границы страны)
ax.plot([0, 100], [0, 0], color='blue', linewidth=4)  # южная граница
ax.plot([0, 0], [0, 100], color='blue', linewidth=4)  # западная граница

# --- Внутренние элементы страны "Аурелия" ---
# Острова
island1 = patches.Circle((10, 10), 3, facecolor='yellow', edgecolor='black')
island2 = patches.Circle((90, 90), 3, facecolor='yellow', edgecolor='black')
ax.add_patch(island1)
ax.add_patch(island2)

# Полуостров (на востоке)
peninsula = patches.Polygon([[100, 40], [120, 50], [100, 60]], closed=True, facecolor='lightblue', edgecolor='black')
ax.add_patch(peninsula)

# Озёра (в центральной части)
lake1 = patches.Circle((50, 70), 5, facecolor='deepskyblue', edgecolor='black')
lake2 = patches.Circle((70, 30), 4, facecolor='deepskyblue', edgecolor='black')
ax.add_patch(lake1)
ax.add_patch(lake2)

# Реки (извилистая синяя линия)
ax.annotate("",
            xy=(20, 0), xycoords='data',
            xytext=(80, 100), textcoords='data',
            arrowprops=dict(arrowstyle="->", color='blue', lw=2, connectionstyle="arc3,rad=-0.5"))

# Леса (зелёные прямоугольники)AAaaaasaz
forest1 = patches.Rectangle((20, 20), 20, 20, facecolor='green', alpha=0.5)
forest2 = patches.Rectangle((60, 60), 20, 20, facecolor='green', alpha=0.5)
ax.add_patch(forest1)
ax.add_patch(forest2)

# Горы (на северо-востоке)
mountains = patches.Polygon([[70, 80], [80, 95], [90, 80]], closed=True, facecolor='saddlebrown', edgecolor='black')
ax.add_patch(mountains)

# Пустыни (на юго-востоке)
desert = patches.Rectangle((60, 0), 40, 30, facecolor='khaki', hatch='//', edgecolor='black', alpha=0.6)
ax.add_patch(desert)

# Степи (на западе)
steppes = patches.Rectangle((0, 40), 20, 40, facecolor='lightyellow', edgecolor='black', alpha=0.5)
ax.add_patch(steppes)

# Пашни (плодородные поля, обозначенные золотыми линиями)
for i in range(5):
    ax.plot([30, 80], [10 + i*2, 10 + i*2], color='goldenrod', linewidth=1)

# Ресурсы (месторождения, обозначенные звёздами)
ax.text(15, 85, '★', fontsize=20, color='red')
ax.text(85, 15, '★', fontsize=20, color='red')

# Автономные регионы (выделены пунктирными рамками)
autonomous = patches.Rectangle((65, 65), 20, 20, linewidth=2, edgecolor='purple', linestyle='--', facecolor='none')
ax.add_patch(autonomous)

# Диаспоры (области проживания этнических меньшинств)
ax.plot(40, 50, marker='o', color='magenta', markersize=10)
ax.text(42, 50, "Диаспора", fontsize=8, color='magenta')

# Разделительные этносы (внутренние этнические границы – пунктирная линия)
ax.plot([0, 100], [55, 55], color='black', linestyle=':', linewidth=2)

# Буферное положение (зона демилитаризации, отображённая щитом и подписью)
ax.text(50, 98, "🛡", fontsize=20, ha='center')
ax.text(50, 105, "Буферное положение", fontsize=12, ha='center', color='darkblue')

# Приграничное положение (утолщённые границы)
ax.plot([0, 0], [0, 100], color='red', linewidth=4)
ax.plot([100, 100], [0, 100], color='red', linewidth=4)

# --- Бонусные элементы ---
# Государства-города (мегаполис)
ax.plot(50, 50, marker='s', color='black', markersize=12)
ax.text(52, 50, "Город", fontsize=10, va='center')

# Комплементарные этносы (две переплетённые окружности)
comp1 = patches.Circle((30, 80), 4, facecolor='cyan', edgecolor='black', alpha=0.5)
comp2 = patches.Circle((34, 80), 4, facecolor='magenta', edgecolor='black', alpha=0.5)
ax.add_patch(comp1)
ax.add_patch(comp2)

# Сильная исполнительная власть (столица)
ax.plot(50, 90, marker='*', color='gold', markersize=15)
ax.text(52, 92, "Столица", fontsize=10, color='darkblue')

# Военный флот (символ корабля на побережье)
ax.text(5, -5, "⛵", fontsize=20)

# Миротворчество (символ мира – олива)
ax.text(90, 95, "☮", fontsize=20, color='green')

# --- Штрафные элементы ---
# Лингвистические чуждые (обозначены знаком «?»)
ax.text(80, 70, "?", fontsize=16, color='brown')

# Некомплементарные этносы (области конфликтов – красные пятна)
ax.add_patch(patches.Rectangle((10, 10), 10, 10, facecolor='red', alpha=0.3))

# Сепаратисты (обозначены треугольником с восклицательным знаком)
ax.text(80, 10, "▲!", fontsize=14, color='darkred')

# Террористическzzzzzzzzxxxxx xxxxxxsssssssssssssssssssss1ая активность (обозначена как «!!!»)
ax.text(30, 30, "!!!", fontsize=14, color='red')

# Настройки отображения
ax.set_xlim(-50, 150)
ax.set_ylim(-25, 130)
ax.set_aspect('equal')
plt.title("Карта государства «Аурелия» с приграничными соседями")
plt.axis('off')
plt.show()
