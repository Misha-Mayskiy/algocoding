import requests


def get_toponym_info():
    server_address = 'http://geocode-maps.yandex.ru/1.x/'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    geocode = 'Красная площадь, 1'

    params = {
        'apikey': api_key,
        'geocode': geocode,
        'format': 'json'
    }

    response = requests.get(server_address, params=params)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        full_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        coordinates = " ".join(toponym["Point"]["pos"].split()[::-1])

        print("Полный адрес:", full_address)
        print("Координаты:", coordinates)
    else:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, response.reason)


if __name__ == '__main__':
    get_toponym_info()
