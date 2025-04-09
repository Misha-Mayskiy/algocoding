import requests
import sys

API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"


def get_coordinates(city_name):
    params = {
        "apikey": API_KEY,
        "geocode": city_name,
        "format": "json"
    }
    try:
        response = requests.get(GEOCODER_API_SERVER, params=params)
        response.raise_for_status()

        json_response = response.json()

        if not json_response["response"]["GeoObjectCollection"]["featureMember"]:
            print(f"Предупреждение: Город '{city_name}' не найден.")
            return None

        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        coords_str = toponym["Point"]["pos"]
        longitude, latitude = map(float, coords_str.split())

        return longitude, latitude

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при запросе для города '{city_name}': {e}")
        return None
    except (KeyError, IndexError):
        print(f"Ошибка: Не удалось извлечь координаты для города '{city_name}' из ответа API.")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка при обработке города '{city_name}': {e}")
        return None


def find_southernmost_city(city_names):
    southernmost_city = None
    min_latitude = float('inf')

    for city in city_names:
        coords = get_coordinates(city.strip())
        if coords:
            longitude, latitude = coords
            if latitude < min_latitude:
                min_latitude = latitude
                southernmost_city = city.strip()

    return southernmost_city


if __name__ == "__main__":
    cities_input = input("Введите названия городов через запятую: ")

    if not cities_input:
        print("Ошибка: Вы не ввели названия городов.")
        sys.exit(1)

    cities_list = cities_input.split(',')

    cities_list = [city for city in cities_list if city.strip()]

    if not cities_list:
        print("Ошибка: Список городов пуст после обработки ввода.")
        sys.exit(1)

    print("\nИдет определение координат...")
    result_city = find_southernmost_city(cities_list)

    if result_city:
        print(f"\nСамый южный город: {result_city}")
    else:
        print("\nНе удалось определить самый южный город из введенного списка.")
