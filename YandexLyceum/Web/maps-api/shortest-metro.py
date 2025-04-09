import requests
import sys

GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"


def get_object_coordinates(address):
    params = {
        "apikey": GEOCODER_API_KEY,
        "geocode": address,
        "format": "json"
    }
    print(f"Ищем координаты для адреса: '{address}'...")
    try:
        response = requests.get(GEOCODER_API_SERVER, params=params)
        response.raise_for_status()
        json_response = response.json()

        feature_member = json_response["response"]["GeoObjectCollection"]["featureMember"]
        if not feature_member:
            print(f"Ошибка: Адрес '{address}' не найден.")
            return None

        toponym = feature_member[0]["GeoObject"]
        coords_str = toponym["Point"]["pos"]
        print(f"Координаты найдены: {coords_str.replace(' ', ',')}")
        return coords_str.replace(' ', ',')

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при запросе координат: {e}")
        return None
    except (KeyError, IndexError):
        print(f"Ошибка: Не удалось извлечь координаты из ответа API для адреса '{address}'.")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка при поиске координат: {e}")
        return None


def find_nearest_object(coords_str, kind):
    params = {
        "apikey": GEOCODER_API_KEY,
        "geocode": coords_str,
        "kind": kind,
        "format": "json",
        "results": 1
    }
    print(f"Ищем ближайший объект типа '{kind}' около координат {coords_str}...")
    try:
        response = requests.get(GEOCODER_API_SERVER, params=params)
        response.raise_for_status()
        json_response = response.json()

        feature_member = json_response["response"]["GeoObjectCollection"]["featureMember"]
        if not feature_member:
            print(f"Рядом с указанными координатами не найдено объектов типа '{kind}'.")
            return None

        nearest_object = feature_member[0]["GeoObject"]
        object_address = nearest_object["metaDataProperty"]["GeocoderMetaData"]["text"]

        print(f"Найден ближайший объект: {object_address}")
        return object_address

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при поиске ближайшего объекта: {e}")
        return None
    except (KeyError, IndexError):
        print("Ошибка: Не удалось извлечь информацию о ближайшем объекте из ответа API.")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка при поиске ближайшего объекта: {e}")
        return None


if __name__ == "__main__":
    address_input = input("Введите адрес: ")

    if not address_input:
        print("Ошибка: Вы не ввели адрес.")
        sys.exit(1)

    coordinates = get_object_coordinates(address_input)

    if coordinates:
        nearest_metro = find_nearest_object(coordinates, "metro")

        if nearest_metro:
            print("-" * 30)
            print(f"Ближайшая станция метро к адресу '{address_input}':")
            print(nearest_metro)
            print("-" * 30)
        else:
            print("-" * 30)
            print(f"Не удалось найти станцию метро рядом с адресом '{address_input}'.")
            print("-" * 30)
    else:
        sys.exit(1)
