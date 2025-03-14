import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, ax = plt.subplots(figsize=(12, 12))

###############################################################################
#                             1. Фон и границы                                #
###############################################################################

# Цвет суши для Аурелии
ax.set_facecolor('#e0dabd')

# Прямоугольник, обозначающий территорию Аурелии (0..10 по обеим осям)
aur_border = patches.Rectangle((0, 0), 10, 10, linewidth=2, edgecolor='black', facecolor='none')
ax.add_patch(aur_border)

# Соседние государства:
#  - Альтания (x < 0)
#  - Зелестия (x > 10)
#  - Бореалия (y > 10)

# Пунктирные линии для границ с соседями
ax.plot([0, 0], [0, 10], linestyle='--', color='black', label="Граница с Альтанией")
ax.plot([10, 10], [0, 10], linestyle='--', color='black', label="Граница с Зелестией")
ax.plot([0, 10], [10, 10], linestyle='--', color='black', label="Граница с Бореалией")

# Подписи соседних стран
ax.text(-1.5, 5, "Альтания", fontsize=12, rotation=90, va='center', ha='center', fontweight='bold')
ax.text(11.5, 5, "Зелестия", fontsize=12, rotation=-90, va='center', ha='center', fontweight='bold')
ax.text(5, 10.5, "Бореалия", fontsize=12, va='center', ha='center', fontweight='bold')

###############################################################################
#        2. Моря, пролив, побережья, острова, полуостров, военный флот        #
###############################################################################

sea_color = '#5d9cec'

# Западное море (слева, x < 0)
ax.add_patch(patches.Rectangle((-5, 0), 5, 10, facecolor=sea_color, zorder=0))
# Южное море (снизу, y < 0)
ax.add_patch(patches.Rectangle((0, -5), 10, 5, facecolor=sea_color, zorder=0))

# Пролив (узкая полоса воды, соединяющая западное и южное моря) в юго-западном углу
strait = patches.Rectangle((0, 0), -1, -1, facecolor=sea_color, zorder=0)
ax.add_patch(strait)
ax.text(-0.5, -0.5, "Пролив\nКрон", fontsize=9, color='white', ha='center', va='center')

# Полуостров Кассия (на востоке, x>9, y ~ 2..4)
peninsula = patches.Rectangle((9.3, 2), 0.7, 2, facecolor='#e0dabd', edgecolor='black')
ax.add_patch(peninsula)
ax.text(9.65, 3, "Полуостров\nКассия", fontsize=9, ha='center', va='center')

# Острова Мист (в юго-западной акватории)
island_positions = [( -1.2, 1 ), ( -1.8, 1.5 ), ( -1.5, 0.5 )]
for i, (ix, iy) in enumerate(island_positions):
    c = patches.Circle((ix, iy), 0.3, facecolor='#e0dabd', edgecolor='black')
    ax.add_patch(c)
ax.text(island_positions[0][0], island_positions[0][1]+0.5, "Острова\nМист", fontsize=9, ha='center')

# Военный флот (символы кораблей у берега)
ax.text(0.5, 0.3, "⛵", fontsize=16, color='white')
ax.text(1, 0.2, "⚓", fontsize=16, color='white')
ax.text(0.7, 0.6, "Военный\nфлот", fontsize=8, color='white')

###############################################################################
#                      3. Озёра, реки, леса, горы, пустыни, степи             #
###############################################################################

# Озёра (два круглых водоёма в центральных районах)
lake1 = patches.Circle((4, 6), 1, facecolor=sea_color, ec='black')
lake2 = patches.Circle((7, 4), 1.2, facecolor=sea_color, ec='black')
ax.add_patch(lake1)
ax.add_patch(lake2)
ax.text(4, 6, "Озеро\nЛуминос", fontsize=9, ha='center', va='center', color='white')
ax.text(7, 4, "Озеро\nСапфир", fontsize=9, ha='center', va='center', color='white')

# Река Вальдис (извилистая линия сверху вниз)
river_x = [3, 3.5, 4, 4.5, 5, 5.5, 5.8, 6, 6.2, 6.5]
river_y = [10, 9, 8, 7, 6, 5, 4.5, 4, 3, 0]
ax.plot(river_x, river_y, color=sea_color, linewidth=3, label="Река Вальдис")
ax.text(3.5, 9, "Река Вальдис", fontsize=9, color='white')

# Леса (зелёные «шишечки»). Примерно в районе (2..4, 6..9)
for _ in range(40):
    x = np.random.uniform(2, 4)
    y = np.random.uniform(6, 9)
    ax.plot(x, y, marker="^", color="darkgreen", markersize=8, alpha=0.7)
ax.text(3, 8.5, "Лес\nТенарис", fontsize=9, color='darkgreen', ha='center')

# Горы (северо-восток, серые треугольники)
for _ in range(10):
    x = np.random.uniform(6, 10)
    y = np.random.uniform(8, 10)
    ax.plot(x, y, marker="^", color="gray", markersize=10)
ax.text(8, 9.5, "Горы\nАйронкрест", fontsize=9, color='gray', ha='center')

# Пустыня Орим (юго-восток). Прямоугольник с сеткой
desert = patches.Rectangle((6, 0), 4, 2, facecolor='khaki', hatch='//', ec='black', alpha=0.4)
ax.add_patch(desert)
ax.text(8, 1, "Пустыня\nОрим", fontsize=9, ha='center', va='center')

# Степи Сольвейг (запад, прямоугольник  (0..2, 5..7) )
steppes = patches.Rectangle((0, 5), 2, 2, facecolor='lightyellow', ec='black', alpha=0.5)
ax.add_patch(steppes)
ax.text(1, 6, "Степи\nСольвейг", fontsize=9, ha='center')

###############################################################################
#                       4. Пашни, ресурсы, автономии, диаспоры                #
###############################################################################

# Пашни (золотые линии, скажем, в прямоугольнике (2..4, 2..3))
for i in range(5):
    y_line = 2.1 + i*0.15
    ax.plot([2, 4], [y_line, y_line], color='goldenrod', linewidth=2)
ax.text(3, 2.5, "Пашни\n(Плодородные поля)", fontsize=9, color='goldenrod', ha='center')

# Ресурсы (месторождения полезных ископаемых, красные звёзды)
resource_coords = [(1, 8), (8, 2), (2, 2)]
for rx, ry in resource_coords:
    ax.text(rx, ry, "★", fontsize=14, color='red')
ax.text(1.9, 1.8, "Ресурсы", fontsize=8, color='red', ha='left')

# Автономная область (рамка). Например, (2..3, 8..9)
auton_region = patches.Rectangle((2, 8), 1, 1, linewidth=2, edgecolor='purple', linestyle='--', facecolor='none')
ax.add_patch(auton_region)
ax.text(2.5, 8.5, "Автономия\nДракенхольм", fontsize=8, ha='center', color='purple')

# Диаспоры. Сделаем отдельную «область» (4..5, 7..8) в виде полупрозрачного прямоугольника + подпись.
diaspora_region = patches.Rectangle((4, 7), 1, 1, facecolor='pink', alpha=0.3, edgecolor='none')
ax.add_patch(diaspora_region)
ax.text(4.5, 7.5, "Диаспоры\n(Лисмир)", fontsize=8, color='darkred', ha='center')

# Разделительные этносы (пунктирная линия внутри страны).
# Пусть идёт от (2, 5.5) до (8, 5.5)
ax.plot([2, 8], [5.5, 5.5], color='black', linestyle=':', linewidth=2)
ax.text(8.1, 5.5, "Разделительная\nэтническая граница", fontsize=8, va='center', color='black')

###############################################################################
#                      5. Буферное и приграничное положение                   #
###############################################################################

# Буферное положение (щит в северной части)
ax.text(5, 9.7, "🛡", fontsize=18, ha='center')
ax.text(5, 9.4, "Буферная зона", fontsize=8, ha='center')

# Приграничное положение — утолщённые контуры самой страны:
border_patch = patches.Rectangle((0, 0), 10, 10, linewidth=3, edgecolor='red', facecolor='none')
ax.add_patch(border_patch)

###############################################################################
#      6. Бонусные элементы: гос-города (несколько), комплементарные этносы,   #
#           сильная исполнительная власть, миротворчество                     #
###############################################################################

# 6.1. Государства-города (два города)
# Первый: Арктон (3,3)
ax.plot(3, 3, marker='P', markersize=12, color='black')
ax.text(3, 2.7, "Гос-во-город\nАрктон", fontsize=8, ha='center', va='top')

# Второй: Валенсия (7.5,7.5)
ax.plot(7.5, 7.5, marker='P', markersize=12, color='black')
ax.text(7.5, 7.2, "Гос-во-город\nВаленсия", fontsize=8, ha='center', va='top')

# 6.2. Комплементарные этносы (два пересекающихся круга)
comp1 = patches.Circle((2.5, 6.5), 0.3, facecolor='cyan', alpha=0.5, edgecolor='black')
comp2 = patches.Circle((2.8, 6.5), 0.3, facecolor='magenta', alpha=0.5, edgecolor='black')
ax.add_patch(comp1)
ax.add_patch(comp2)
ax.text(2.65, 6.2, "Комплементарные\nэтносы", fontsize=8, ha='center')

# 6.3. Сильная исполнительная власть (у столицы).
# Столица: (5,5) — звезда. Дополнительно рядом знак "⚜" или "🏛"
ax.plot(5, 5, marker='*', markersize=20, color='gold')
ax.text(5, 5.3, "Столица\n(Сильная власть)", fontsize=9, ha='center', color='darkblue')
ax.text(5.3, 5, "🏛", fontsize=14, color='darkblue', va='center')

# 6.4. Миротворчество (символ «☮» рядом с северной границей)
ax.text(6, 9.5, "☮", fontsize=16, color='green')
ax.text(6.3, 9.5, "Миротворч.\nцентр", fontsize=8, color='green', va='center')

###############################################################################
#                  7. Штрафные элементы: язык, этносы, сепаратисты, террор    #
###############################################################################

# 7.1. Лингвистические чуждые (знак «?» возле населённого пункта)
ax.text(2, 4.5, "?", fontsize=14, color='brown')
ax.text(2.2, 4.5, "Лингвист.\nчуждые", fontsize=8, color='brown', va='center')

# 7.2. Некомплементарные этносы (красные пятна, например, (8..9, 6..7))
for _ in range(10):
    x = np.random.uniform(8, 9)
    y = np.random.uniform(6, 7)
    ax.scatter(x, y, color='red', s=20, alpha=0.6)
ax.text(8.5, 7.1, "Некомплементарные\nэтносы", fontsize=8, color='red', ha='center')

# 7.3. Сепаратисты (треугольник с восклицательным знаком)
ax.text(8.5, 3.5, "▲!", fontsize=12, color='darkred')
ax.text(8.7, 3.5, "Сепаратисты", fontsize=8, color='darkred', va='center')

# 7.4. Террористическая активность (красные вспышки)
ax.text(4.5, 2.5, "!!!", fontsize=14, color='red')
ax.text(4.7, 2.5, "Террорист.\nактивность", fontsize=8, color='red', va='center')

###############################################################################
#                        Итоговые настройки и легенда                         #
###############################################################################

ax.set_xlim(-2, 12)
ax.set_ylim(-2, 12)
ax.set_xticks([])
ax.set_yticks([])
plt.title("Карта «Аурелия» со всеми выбранными элементами", fontsize=14)

# Формируем объекты для легенды (фиктивные, чтобы отразить нужные подписи)
legend_patches = [
    patches.Patch(color=sea_color, label="Море"),
    patches.Patch(color='lightyellow', label="Степи"),
    patches.Patch(color='khaki', label="Пустыня"),
    patches.Patch(color='darkgreen', label="Леса"),
    patches.Patch(color='gray', label="Горы"),
    patches.Patch(color='goldenrod', label="Пашни"),
    patches.Patch(color='pink', alpha=0.3, label="Диаспоры"),
    patches.Patch(color='none', hatch='//', label="Текстура пустыни", edgecolor='black'),
]

ax.legend(handles=legend_patches, loc="lower right", fontsize=9, frameon=True)
plt.show()
