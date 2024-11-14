# Артефакт древних медведй:     artefact        = X
# Прототип дрона-разведчика:    drone           = X * 5
# Лазерный резак:               laser_cutter    = X * 5 / 3
# Бочонок энергомеда:           barrel_honey    = X * 5 * 12
# Набор для хакинга:            hacking_pack    = X * 5 * 12 / 4
# Кристалл памяти:              crystal_memory  = X * 5 * 12 / 4 * 13

artefact, drone, laser_cutter, barrel_honey, hacking_pack, crystal_memory = 0, 0, 0, 0, 0, 0

find_ans = False
for i in range(10, 10000):
    for j in range(1, i):
        artefact = j / i
        drone = artefact * 5
        laser_cutter = artefact * 5 / 3
        barrel_honey = artefact * 5 * 12
        hacking_pack = artefact * 5 * 12 / 4
        crystal_memory = artefact * 5 * 12 / 4 * 13

        if artefact + drone + laser_cutter + barrel_honey + hacking_pack + crystal_memory == 1:
            print(i, j)
            find_ans = True
            break
    if find_ans:
        break

print(artefact, drone, laser_cutter, barrel_honey, hacking_pack, crystal_memory, sep="\n")
# hacking_pack cost = 19
# barrel_honey cost = 5 => 5 barrel_honey = 25
# laser_cutter cost = 167 => 2 laser_cutter = 334