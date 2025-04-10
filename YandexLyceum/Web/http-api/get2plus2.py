import requests
import sys
import json

try:
    server_address = input()
    if server_address.endswith('/'):
        server_address = server_address[:-1]

    server_port = int(input())
    a = int(input())
    b = int(input())
except ValueError:
    print("Ошибка: Порт, a и b должны быть целыми числами.")
    sys.exit(1)
except EOFError:
    print("Ошибка: Неожиданный конец ввода.")
    sys.exit(1)

base_url = f"{server_address}:{server_port}"

request_params = {
    "a": a,
    "b": b
}

try:
    response = requests.get(base_url, params=request_params)
    response.raise_for_status()
    data = response.json()

    if 'result' not in data or 'check' not in data:
        print("Ошибка: В ответе сервера отсутствуют ключи 'result' или 'check'.")
        sys.exit(1)

    result_list = data['result']
    check_string = data['check']

    if not isinstance(result_list, list):
        print(f"Ошибка: Ожидался список по ключу 'result', получено: {type(result_list)}")
        sys.exit(1)

    sorted_result = sorted(result_list)
    output_numbers = ' '.join(map(str, sorted_result))

    print(output_numbers)
    print(check_string)

except requests.exceptions.ConnectionError:
    print(f"Ошибка: Не удалось установить соединение с {base_url}")
    sys.exit(1)
except requests.exceptions.Timeout:
    print(f"Ошибка: Превышено время ожидания ответа от {base_url}")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")
    sys.exit(1)
except json.JSONDecodeError:
    print("Ошибка: Не удалось разобрать JSON из ответа сервера.")
    print("Полученный текст:", response.text)
    sys.exit(1)
except Exception as e:
    print(f"Непредвиденная ошибка: {e}")
    sys.exit(1)
