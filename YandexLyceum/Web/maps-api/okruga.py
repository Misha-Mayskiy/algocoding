import requests


def get_federal_district(city):
    server_address = 'http://geocode-maps.yandex.ru/1.x/'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'

    params = {
        'apikey': api_key,
        'geocode': city,
        'format': 'json',
        'kind': 'district',
        'results': 1,
        'lang': 'ru_RU'
    }

    response = requests.get(server_address, params=params)
    if response.status_code == 200:
        json_response = response.json()
        try:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            admin_areas = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]

            federal_district = None
            region = None

            full_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]

            for component in admin_areas:
                kind = component["kind"]
                name = component["name"]

                if kind == "province" and ("федеральный округ" in name.lower() or "фо" in name.lower()):
                    federal_district = name

                if kind == "province" and region is None:
                    region = name

            if federal_district is None and region:
                region_params = {
                    'apikey': api_key,
                    'geocode': region,
                    'format': 'json',
                    'results': 1,
                    'lang': 'ru_RU'
                }

                region_response = requests.get(server_address, params=region_params)
                if region_response.status_code == 200:
                    region_data = region_response.json()
                    try:
                        region_object = region_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                        region_address = region_object["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]

                        for component in region_address:
                            if "федеральный округ" in component["name"].lower():
                                federal_district = component["name"]
                                break
                    except (IndexError, KeyError):
                        pass

            return city, full_address, region, federal_district
        except (IndexError, KeyError) as e:
            return city, None, None, f"Ошибка обработки данных: {str(e)}"
    else:
        return city, None, None, f"Ошибка запроса: {response.status_code}"


if __name__ == '__main__':
    cities = ["Хабаровск", "Уфа", "Нижний Новгород", "Калининград"]

    for city in cities:
        city_name, address, region, district = get_federal_district(city)
        print(f"Город: {city_name}")

        if address:
            print(f"Полный адрес: {address}")

        if region:
            print(f"Регион: {region}")

        if district and "федеральный округ" in district.lower():
            print(f"Федеральный округ: {district}")
        else:
            print("Федеральный округ: не найден в ответе API")

        print("-" * 60)
