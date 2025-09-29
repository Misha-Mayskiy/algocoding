import requests
import base64
import json
import asyncio
import websockets
import random
import os
import logging
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# --- Конфигурация и константы ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

GODVILLE_LOGIN = os.getenv('GODVILLE_LOGIN')
GODVILLE_PASSWORD = os.getenv('GODVILLE_PASSWORD')

LOGIN_URL = 'https://godville.net/login/login'
SUPERHERO_URL = 'https://godville.net/superhero'
BASE_URL = 'https://godville.net'
LOGIN_SUCCESS_CHECK_ELEMENT_ID = 'axe'
WEBSOCKET_URL_KEY = 'u1'
MIN_ACTION_INTERVAL_SEC = 120
MAX_ACTION_INTERVAL_SEC = 300
RESTART_INITIAL_DELAY_SEC = 15
RESTART_MAX_DELAY_SEC = 300

# --- Глобальные переменные для управления сессией ---
session = None
websocket_url = None


# --- Шаг 1: Авторизация ---
def login_and_get_session():
    """Выполняет вход на сайт и сохраняет сессию. Возвращает True в случае успеха."""
    global session
    if session:
        session.close()

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Referer': LOGIN_URL,
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Origin': BASE_URL
    })

    login_data = {'username': GODVILLE_LOGIN, 'password': GODVILLE_PASSWORD, 'login': 'Войти'}

    logging.info("Попытка авторизации...")
    try:
        login_response = session.post(LOGIN_URL, data=login_data, timeout=15, allow_redirects=True)
        login_response.raise_for_status()

        if LOGIN_SUCCESS_CHECK_ELEMENT_ID not in login_response.text:
            logging.error("Ошибка авторизации. Проверьте логин/пароль.")
            return False

        logging.info("Авторизация прошла успешно.")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Сетевая ошибка при авторизации: {e}")
        return False


# --- Шаг 2: Получение URL для WebSocket ---
def get_websocket_url():
    """Извлекает и декодирует URL для подключения. Возвращает URL."""
    global websocket_url
    logging.info("Получение URL для WebSocket...")
    try:
        hero_page_response = session.get(SUPERHERO_URL, timeout=15)
        hero_page_response.raise_for_status()

        if LOGIN_SUCCESS_CHECK_ELEMENT_ID not in hero_page_response.text:
            logging.warning("Сессия могла истечь. Не удалось подтвердить авторизацию.")
            return None

        soup = BeautifulSoup(hero_page_response.text, 'html.parser')
        axe_div = soup.find('div', {'id': LOGIN_SUCCESS_CHECK_ELEMENT_ID})

        if not axe_div:
            logging.error("Не удалось найти элемент 'axe' на странице.")
            return None

        decoded_data = json.loads(base64.b64decode(axe_div.text.strip()).decode('utf-8'))

        url = decoded_data.get(WEBSOCKET_URL_KEY) or decoded_data.get('u')
        if not url:
            logging.error(f"Ключ для URL не найден в данных 'axe'.")
            return None

        websocket_url = url
        logging.info(f"URL для WebSocket успешно получен: {websocket_url}")
        return url
    except Exception as e:
        logging.error(f"Ошибка при получении или обработке URL: {e}")
        return None


# --- Шаг 3: Основная логика ---
async def main_manager():
    """Главный управляющий процесс. Перезапускает всё с нуля, если что-то пошло не так."""
    backoff_delay = RESTART_INITIAL_DELAY_SEC

    while True:
        if login_and_get_session() and (ws_url := get_websocket_url()):
            cookies = session.cookies.get_dict()
            await websocket_logic(ws_url, cookies)

        logging.info(f"Повторная попытка через {backoff_delay} секунд.")
        await asyncio.sleep(backoff_delay)
        backoff_delay = min(backoff_delay * 1.5, RESTART_MAX_DELAY_SEC)


async def websocket_logic(uri, cookies):
    """Управляет WebSocket соединением. При разрыве возвращает управление менеджеру."""
    cookie_str = '; '.join([f'{name}={value}' for name, value in cookies.items()])
    headers = {
        'Cookie': cookie_str,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Origin': BASE_URL
    }

    tasks = []
    try:
        async with websockets.connect(uri, extra_headers=headers) as websocket:
            logging.info("\nУспешно подключено к WebSocket серверу. Начинаю работу.")

            listen_task = asyncio.create_task(listen_server(websocket))
            action_task = asyncio.create_task(send_actions(websocket))
            ping_task = asyncio.create_task(send_pings(websocket))

            tasks = [listen_task, action_task, ping_task]
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                exc = task.exception()
                if exc:
                    raise exc

    except websockets.exceptions.ConnectionClosed as e:
        logging.warning(f"Соединение WebSocket было закрыто сервером: {e}. Перезапускаюсь.")
    except Exception as e:
        logging.error(f"Произошла ошибка в работе WebSocket: {e}. Перезапускаюсь.")
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


async def listen_server(websocket):
    """Асинхронно принимает и выводит сообщения от сервера."""
    async for message in websocket:
        logging.info(f"<-- Получено от сервера: {message}")


async def send_actions(websocket):
    """Асинхронно отправляет команды влияния, имитируя человеческое поведение."""
    while True:
        try:
            if random.randint(1, 10) == 1:
                sleep_duration = random.uniform(3600, 14400)  # 1-4 часа
                logging.info(f"Имитация сна. Пауза на {sleep_duration / 3600:.1f} часов.")
                await asyncio.sleep(sleep_duration)

            wait_time = random.uniform(MIN_ACTION_INTERVAL_SEC, MAX_ACTION_INTERVAL_SEC)
            logging.info(f"--> Следующее влияние через {wait_time:.0f} сек.")
            await asyncio.sleep(wait_time)

            action = random.choice(["good", "bad"])
            command = {"type": "god_action", "action": action}

            await websocket.send(json.dumps(command))
            logging.info(f"--> Отправлена команда: {json.dumps(command)}")

        except asyncio.CancelledError:
            break
        except websockets.exceptions.ConnectionClosed:
            logging.warning("--> Попытка отправки команды не удалась: соединение закрыто.")
            break


async def send_pings(websocket):
    """Периодически отправляет ping-сообщения для поддержания соединения."""
    while True:
        try:
            await asyncio.sleep(45)
            await websocket.send("2")  # Пользовательский ping-сигнал
            logging.info("--> Отправлен ping-сигнал.")
        except asyncio.CancelledError:
            break
        except websockets.exceptions.ConnectionClosed:
            logging.warning("--> Попытка отправки ping не удалась: соединение закрыто.")
            break


# --- Точка входа в программу ---
if __name__ == "__main__":
    if not GODVILLE_LOGIN or not GODVILLE_PASSWORD:
        exit()
    try:
        asyncio.run(main_manager())
    except KeyboardInterrupt:
        logging.info("Программа остановлена пользователем.")
