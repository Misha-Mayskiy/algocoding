import requests
import sys
from distance import lonlat_distance

GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"


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
        print(f"Ошибка сети при запросе координат для '{address}': {e}")
        return None
    except (KeyError, IndexError):
        print(f"Ошибка: Не удалось извлечь координаты из ответа API для адреса '{address}'.")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка при поиске координат для '{address}': {e}")
        return None


if __name__ == "__main__":
    home_address = input("Введите адрес дома: ")
    if not home_address:
        print("Ошибка: Адрес дома не введен.")
        sys.exit(1)

    school_address = input("Введите адрес школы: ")
    if not school_address:
        print("Ошибка: Адрес школы не введен.")
        sys.exit(1)

    home_coords = get_coordinates(home_address)
    if home_coords is None:
        sys.exit(1)

    school_coords = get_coordinates(school_address)
    if school_coords is None:
        sys.exit(1)

    print("\nРасчет расстояния...")
    distance_meters = lonlat_distance(home_coords, school_coords)

    distance_km = distance_meters / 1000
    print("-" * 40)
    print(f"Приблизительное расстояние между:")
    print(f"  Дом ({home_address})")
    print(f"  Школа ({school_address})")
    print(f"\nСоставляет: {distance_meters:.2f} метров (~{distance_km:.2f} км)")
    print("-" * 40)
