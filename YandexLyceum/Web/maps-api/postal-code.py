import requests


def get_postal_index():
    url = 'https://geocode-maps.yandex.ru/1.x/'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    address = 'Петровка, 38'

    params = {
        'apikey': api_key,
        'geocode': address,
        'format': 'json'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        geo_object = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        address_metadata = geo_object["metaDataProperty"]["GeocoderMetaData"]["Address"]

        postal_code = address_metadata.get("postal_code")
        if postal_code:
            print("Почтовый индекс:", postal_code)
        else:
            print("Почтовый индекс не найден")
    except (IndexError, KeyError):
        print("Ошибка при разборе данных геокодера")
    except requests.RequestException as e:
        print(f"Ошибка HTTP-запроса: {e}")


if __name__ == '__main__':
    get_postal_index()
