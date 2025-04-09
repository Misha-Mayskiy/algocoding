import pygame
import requests
import sys
import os
import math

STATIC_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
STATIC_API_SERVER = "https://static-maps.yandex.ru/v1?"
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 450
TEMP_IMAGE_FILE = "path_map.png"
EARTH_RADIUS_KM = 6371

PATH_POINTS = [
    (37.617635, 55.755814),  # Красная площадь
    (37.621618, 55.758613),  # ГУМ
    (37.616879, 55.760080),  # Никольская улица
    (37.617130, 55.763458),  # Метро "Театральная" (выход)
    (37.618695, 55.765708),  # Большой театр
    (37.610918, 55.763669),  # ЦУМ
    (37.608118, 55.760871)  # Ул. Петровка / Кузнецкий мост
]


def haversine(lon1, lat1, lon2, lat2):
    lon1_rad, lat1_rad, lon2_rad, lat2_rad = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Формула Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = EARTH_RADIUS_KM * c
    return distance


def calculate_path_details(points):
    if len(points) < 2:
        return 0, None

    total_length = 0
    segment_lengths = []

    for i in range(len(points) - 1):
        lon1, lat1 = points[i]
        lon2, lat2 = points[i + 1]
        segment_dist = haversine(lon1, lat1, lon2, lat2)
        segment_lengths.append(segment_dist)
        total_length += segment_dist

    half_length = total_length / 2
    cumulative_length = 0
    midpoint_index = 0
    min_diff = float('inf')

    for i in range(len(points)):
        diff_to_mid = abs(cumulative_length - half_length)

        if diff_to_mid < min_diff:
            min_diff = diff_to_mid
            midpoint_index = i

        if i < len(segment_lengths):
            cumulative_length += segment_lengths[i]

    diff_to_mid_last = abs(total_length - half_length)
    if diff_to_mid_last < min_diff:
        midpoint_index = len(points) - 1

    midpoint_coords = points[midpoint_index]
    return total_length, midpoint_coords


def create_static_api_request(path_points, midpoint_coords):
    path_str = "c:ff0000ff,w:4"
    for lon, lat in path_points:
        path_str += f",{lon:.6f},{lat:.6f}"
    midpoint_str = f"{midpoint_coords[0]:.6f},{midpoint_coords[1]:.6f},pm2blm"

    params = {
        "apikey": STATIC_API_KEY,
        "l": "map",
        "pl": path_str,
        "pt": midpoint_str
    }
    return STATIC_API_SERVER, params


def fetch_and_save_map(url, params):
    print("Запрос карты из Static API...")
    try:
        response = requests.get(url, params=params)
        print(f"URL запроса: {response.url}")
        response.raise_for_status()

        with open(TEMP_IMAGE_FILE, "wb") as file:
            file.write(response.content)
        print("Карта успешно загружена и сохранена.")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при запросе карты: {e}")
        return False
    except Exception as e:
        print(f"Непредвиденная ошибка при получении/сохранении карты: {e}")
        return False


def display_map_and_wait():
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Путь на карте")

        image = pygame.image.load(TEMP_IMAGE_FILE)
        screen.blit(image, (0, 0))
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = False


    except pygame.error as e:
        print(f"Ошибка Pygame при отображении: {e}")
    except FileNotFoundError:
        print(f"Ошибка: Не найден временный файл {TEMP_IMAGE_FILE}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    if len(PATH_POINTS) < 2:
        print("Ошибка: Путь должен содержать как минимум две точки.")
        sys.exit(1)

    total_distance, middle_point = calculate_path_details(PATH_POINTS)

    if middle_point is None:
        print("Не удалось определить среднюю точку.")
        sys.exit(1)

    print(f"Заданный путь:")
    for i, p in enumerate(PATH_POINTS):
        print(f"  Точка {i + 1}: ({p[0]:.6f}, {p[1]:.6f})")
    print(f"\nОбщая длина пути: {total_distance:.3f} км")
    print(f"Точка, ближайшая к середине пути: ({middle_point[0]:.6f}, {middle_point[1]:.6f})")

    api_url, api_params = create_static_api_request(PATH_POINTS, middle_point)

    if fetch_and_save_map(api_url, api_params):
        display_map_and_wait()
    else:
        print("Не удалось загрузить карту.")

    if os.path.exists(TEMP_IMAGE_FILE):
        try:
            os.remove(TEMP_IMAGE_FILE)
            print(f"Временный файл {TEMP_IMAGE_FILE} удален.")
        except OSError as e:
            print(f"Ошибка при удалении временного файла: {e}")

    sys.exit(0)
