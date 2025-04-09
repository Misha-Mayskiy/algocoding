import requests
import sys
import math


def haversine_distance(point1, point2):
    lon1, lat1 = point1
    lon2, lat2 = point2
    R = 6371.0
    lon1_rad, lat1_rad, lon2_rad, lat2_rad = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"

OSTANKINO_TOWER_COORDS = (37.6117, 55.8197)
OSTANKINO_TOWER_HEIGHT_M = 525
LINE_OF_SIGHT_FACTOR = 3.6


def get_coordinates(address):
    params = {
        "apikey": GEOCODER_API_KEY,
        "geocode": address,
        "format": "json"
    }
    print(f"\nПолучение координат для адреса: '{address}'...")
    try:
        response = requests.get(GEOCODER_API_SERVER, params=params)
        response.raise_for_status()
        json_response = response.json()

        feature_member = json_response["response"]["GeoObjectCollection"]["featureMember"]
        if not feature_member:
            print(f"Ошибка: Адрес '{address}' не найден Геокодером.")
            return None

        toponym = feature_member[0]["GeoObject"]
        coords_str = toponym["Point"]["pos"]
        longitude, latitude = map(float, coords_str.split())
        print(f"Координаты найдены: ({longitude:.6f}, {latitude:.6f})")
        return (longitude, latitude)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при запросе координат: {e}")
        return None
    except (KeyError, IndexError):
        print(f"Ошибка: Не удалось извлечь координаты из ответа API для '{address}'.")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка при поиске координат: {e}")
        return None


def calculate_required_antenna_height(distance_km, h1_m):
    sqrt_h1 = math.sqrt(h1_m)
    term = (distance_km / LINE_OF_SIGHT_FACTOR) - sqrt_h1
    if term <= 0:
        return 0.0
    else:
        h2_m = term ** 2
        return h2_m


if __name__ == "__main__":
    target_address = input("Введите адрес или название населенного пункта для расчета: ")
    if not target_address:
        print("Ошибка: Адрес не введен.")
        sys.exit(1)

    target_coords = get_coordinates(target_address)
    if target_coords is None:
        sys.exit(1)

    print("\nРасчет расстояния до Останкинской телебашни...")
    distance_l_km = haversine_distance(OSTANKINO_TOWER_COORDS, target_coords)
    print(f"Расстояние: {distance_l_km:.2f} км")

    print("\nРасчет минимальной высоты приемной антенны...")
    required_h2_m = calculate_required_antenna_height(distance_l_km, OSTANKINO_TOWER_HEIGHT_M)

    print("-" * 50)
    print(f"Для приема сигнала с Останкинской телебашни (высота {OSTANKINO_TOWER_HEIGHT_M} м)")
    print(f"в точке '{target_address}' (расстояние {distance_l_km:.2f} км),")
    print(f"минимальная высота приемной антенны должна быть: {required_h2_m:.2f} метров.")
    print("-" * 50)
