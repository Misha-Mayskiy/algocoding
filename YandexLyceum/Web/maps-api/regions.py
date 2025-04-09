import requests


def get_region_for_city(city):
    server_address = 'http://geocode-maps.yandex.ru/1.x/'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'

    params = {
        'apikey': api_key,
        'geocode': city,
        'format': 'json',
        'kind': 'locality',
        'results': 1,
        'lang': 'ru_RU'
    }

    try:
        response = requests.get(server_address, params=params)
        if response.status_code != 200:
            return city, None, f"Ошибка запроса: {response.status_code}"

        json_response = response.json()
        if not json_response["response"]["GeoObjectCollection"]["featureMember"]:
            return city, None, "Город не найден"

        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        full_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        address_components = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]

        region = None
        for component in address_components:
            if component["kind"] in ["province", "area"]:
                region = component["name"]
                if any(x in region.lower() for x in
                       ["область", "край", "республика", "автономный округ", "автономная область"]):
                    break

        return city, region, full_address
    except Exception as e:
        return city, None, f"Ошибка обработки данных: {str(e)}"


if __name__ == '__main__':
    cities = ["Барнаул", "Мелеуз", "Йошкар-Ола"]

    for city in cities:
        city_name, region, address_info = get_region_for_city(city)
        print(f"Город: {city_name}")
        if isinstance(address_info, str) and ("Ошибка" in address_info or "не найден" in address_info):
            print(f"Статус: {address_info}")
        else:
            print(f"Полный адрес: {address_info}")

        if region:
            print(f"Область/Регион: {region}")
        else:
            print("Область/Регион: не определена")
        print("-" * 60)
