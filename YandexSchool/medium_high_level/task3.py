import sys


# Функция для подсчета манхэтенского расстояния
def get_min_dist(r1_xld, r1_yld, r1_xru, r1_yru, r2_xld, r2_yld, r2_xru, r2_yru):
    dist_x = 0
    if r1_xru < r2_xld:
        dist_x = r2_xld - r1_xru
    elif r2_xru < r1_xld:
        dist_x = r1_xld - r2_xru
    dist_y = 0
    if r1_yru < r2_yld:
        dist_y = r2_yld - r1_yru
    elif r2_yru < r1_yld:
        dist_y = r1_yld - r2_yru

    return dist_x + dist_y


def liza_vibes():
    field_width, field_height = map(int, sys.stdin.readline().split())
    num_photos = int(sys.stdin.readline())

    if num_photos == 0:
        return "Yes"

    photo_zones = []
    for i in range(num_photos):
        orig_xld, orig_yld, orig_xru, orig_yru = map(int, sys.stdin.readline().split())
        cut_xld = max(1, orig_xld)
        cut_yld = max(1, orig_yld)
        cut_xru = min(field_width, orig_xru)
        cut_yru = min(field_height, orig_yru)

        photo_zones.append((cut_xld, cut_yld, cut_xru, cut_yru))

        if i == 0 and (cut_xld > cut_xru or cut_yld > cut_yru):
            return "No"

    # Если повезет, то кайф O(N), иначе O(N*W*H) - смэрть от TL-инсульта
    for i in range(num_photos - 1):
        now_zone = photo_zones[i]
        next_zone = photo_zones[i + 1]
        min_dist = get_min_dist(*now_zone, *next_zone)
        if min_dist > 1:
            return "No"

    can_liza_reach_now = [[False] * (field_height + 2) for _ in range(field_width + 2)]
    can_liza_reach_next = [[False] * (field_height + 2) for _ in range(field_width + 2)]

    start_xld, start_yld, start_xru, start_yru = photo_zones[0]
    can_liza_start_zone = False

    if start_xld <= start_xru and start_yld <= start_yru:
        for x in range(start_xld, start_xru + 1):
            for y in range(start_yld, start_yru + 1):
                can_liza_reach_now[x][y] = True
                can_liza_start_zone = True

    if not can_liza_start_zone:
        return "No"

    if num_photos == 1:
        return "Yes"

    for i in range(num_photos - 1):

        for x_idx in range(1, field_width + 1):
            for y_idx in range(1, field_height + 1):
                can_liza_reach_next[x_idx][y_idx] = False

        next_zone_possible = False
        next_xld, next_yld, next_xru, next_yru = photo_zones[i + 1]

        if next_xld > next_xru or next_yld > next_yru:
            return "No"

        for x in range(1, field_width + 1):
            for y in range(1, field_height + 1):
                if can_liza_reach_now[x][y]:
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        neighbor_x, neighbor_y = x + dx, y + dy
                        if next_xld <= neighbor_x <= next_xru and next_yld <= neighbor_y <= next_yru:
                            if not can_liza_reach_next[neighbor_x][neighbor_y]:
                                can_liza_reach_next[neighbor_x][neighbor_y] = True
                                next_zone_possible = True

        if not next_zone_possible:
            return "No"

        can_liza_reach_now, can_liza_reach_next = can_liza_reach_next, can_liza_reach_now

    return "Yes"


print(liza_vibes())
