import pygame
import requests
import sys
import os

API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
STATIC_API_SERVER = "https://static-maps.yandex.ru/v1?"
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 450
TEMP_IMAGE_FILE = "current_slide.png"

SLIDES_DATA = [
    {  # 1. Москва, Кремль и окрестности (Схема)
        "ll": "37.6176,55.7520",
        "spn": "0.015,0.01",
        "l": "map"  # Было map
    },
    {  # 2. Санкт-Петербург, Дворцовая площадь (Схема)
        "ll": "30.3141,59.9386",
        "spn": "0.01,0.005",
        "l": "map"  # Было skl
    },
    {  # 3. Озеро Байкал, Ольхон (Схема)
        "ll": "107.367,53.150",
        "spn": "2.0,1.0",
        "l": "map"  # Было sat
    },
    {  # 4. Гора Эверест (Схема)
        "ll": "86.9250,27.9881",
        "spn": "0.1,0.05",
        "l": "map"  # Было skl
    },
    {  # 5. Большой Каньон, США (Схема)
        "ll": "-112.1129,36.1069",
        "spn": "0.5,0.2",
        "l": "map"  # Было map
    }
]


def fetch_and_save_map(params):
    map_params = {"apikey": API_KEY}
    map_params.update(params)

    print(f"Загрузка слайда с параметрами: {params}")
    try:
        response = requests.get(STATIC_API_SERVER, params=map_params)
        response.raise_for_status()

        with open(TEMP_IMAGE_FILE, "wb") as file:
            file.write(response.content)
        print("Слайд успешно загружен и сохранен.")
        return True

    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            print(f"Ошибка сети при запросе карты: {e} (URL: {e.response.url})")
        else:
            print(f"Ошибка сети при запросе карты: {e}")
        return False
    except Exception as e:
        print(f"Непредвиденная ошибка при получении/сохранении карты: {e}")
        return False


def load_and_display_map(screen):
    try:
        image = pygame.image.load(TEMP_IMAGE_FILE)
        screen.blit(image, (0, 0))
        pygame.display.flip()
        print("Слайд отображен.")
        return image
    except pygame.error as e:
        print(f"Ошибка загрузки или отображения изображения: {e}")
        return None
    except FileNotFoundError:
        print(f"Ошибка: Временный файл {TEMP_IMAGE_FILE} не найден.")
        return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Слайд-шоу карт")

    current_slide_index = 0
    running = True

    if not fetch_and_save_map(SLIDES_DATA[current_slide_index]):
        print("Не удалось загрузить начальный слайд. Выход.")
        running = False
    else:
        load_and_display_map(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                current_slide_index = (current_slide_index + 1) % len(SLIDES_DATA)
                if fetch_and_save_map(SLIDES_DATA[current_slide_index]):
                    load_and_display_map(screen)
                else:
                    print(f"Не удалось загрузить слайд {current_slide_index}. Показ предыдущего слайда.")

    pygame.quit()
    if os.path.exists(TEMP_IMAGE_FILE):
        try:
            os.remove(TEMP_IMAGE_FILE)
            print(f"Временный файл {TEMP_IMAGE_FILE} удален.")
        except OSError as e:
            print(f"Ошибка при удалении временного файла: {e}")
    sys.exit()


if __name__ == '__main__':
    main()
