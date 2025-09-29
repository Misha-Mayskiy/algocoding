import requests
import base64
import json
import asyncio
import socketio
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
sio = socketio.AsyncClient(logger=False, engineio_logger=False)
shutdown_event = asyncio.Event()


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
        'Accept-Language': 'ru-RU,ru;q=0.9'
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
    """Извлекает и декодирует URL для подключения. Возвращает кортеж (url, path)."""
    logging.info("Получение URL для WebSocket...")
    try:
        hero_page_response = session.get(SUPERHERO_URL, timeout=15)
        hero_page_response.raise_for_status()

        if LOGIN_SUCCESS_CHECK_ELEMENT_ID not in hero_page_response.text:
            logging.warning("Сессия могла истечь. Не удалось подтвердить авторизацию.")
            return None, None

        soup = BeautifulSoup(hero_page_response.text, 'html.parser')
        axe_div = soup.find('div', {'id': LOGIN_SUCCESS_CHECK_ELEMENT_ID})

        if not axe_div:
            logging.error("Не удалось найти элемент 'axe' на странице.")
            return None, None

        decoded_data = json.loads(base64.b64decode(axe_div.text.strip()).decode('utf-8'))

        url_raw = decoded_data.get(WEBSOCKET_URL_KEY)
        if not url_raw:
            logging.error(f"Ключ '{WEBSOCKET_URL_KEY}' не найден в данных 'axe'.")
            return None, None

        path_start = url_raw.find('/ws')
        if path_start == -1:
            logging.error(f"Не удалось определить путь из URL: {url_raw}")
            return None, None

        url = url_raw[:path_start]
        path = url_raw[path_start:]

        logging.info(f"URL: {url}, Path: {path}")
        return url, path
    except Exception as e:
        logging.error(f"Ошибка при получении или обработке URL: {e}")
        return None, None


# --- Шаг 3: Логика Socket.IO ---
@sio.event
async def connect():
    logging.info("Успешно подключено к серверу Socket.IO!")


@sio.event
async def disconnect():
    logging.warning("Соединение с сервером Socket.IO разорвано.")
    shutdown_event.set()


@sio.on('*')
async def catch_all(event, data):
    logging.info(f"<-- Получено событие '{event}': {data}")


async def send_actions():
    """Асинхронно отправляет команды влияния, имитируя человеческое поведение."""
    while not shutdown_event.is_set():
        try:
            # С вероятностью 10% бот "уснёт" на 1-4 часа
            if random.randint(1, 10) == 1:
                sleep_duration = random.uniform(3600, 14400)
                logging.info(f"Имитация сна. Пауза на {sleep_duration / 3600:.1f} часов.")
                await asyncio.sleep(sleep_duration)

            wait_time = random.uniform(MIN_ACTION_INTERVAL_SEC, MAX_ACTION_INTERVAL_SEC)
            logging.info(f"--> Следующее влияние через {wait_time:.0f} сек.")
            await asyncio.sleep(wait_time)

            action = random.choice(["good", "bad"])
            command = {"type": "god_action", "action": action}

            await sio.emit('msg', command)
            logging.info(f"--> Отправлена команда: {json.dumps(command)}")

        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.error(f"Ошибка в цикле отправки команд: {e}")
            shutdown_event.set()
            break


# --- Главный управляющий цикл ---
async def main_manager():
    """Управляет полным циклом работы и его перезапуском."""
    backoff_delay = RESTART_INITIAL_DELAY_SEC

    while True:
        shutdown_event.clear()

        if login_and_get_session() and (url_data := get_websocket_url()) and url_data[0]:
            url, path = url_data
            try:
                cookies = session.cookies.get_dict()
                await sio.connect(
                    url,
                    transports=['websocket'],
                    headers={'Cookie': '; '.join([f'{k}={v}' for k, v in cookies.items()])},
                    socketio_path=path
                )

                backoff_delay = RESTART_INITIAL_DELAY_SEC  # Сброс задержки при успехе

                action_task = asyncio.create_task(send_actions())
                await shutdown_event.wait()
                action_task.cancel()
                await sio.disconnect()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Ошибка подключения к Socket.IO: {e}")

        logging.info(f"Повторная попытка через {backoff_delay} секунд.")
        await asyncio.sleep(backoff_delay)
        backoff_delay = min(backoff_delay * 1.5, RESTART_MAX_DELAY_SEC)  # Экспоненциальная задержка


# --- Точка входа ---
if __name__ == "__main__":
    if not GODVILLE_LOGIN or not GODVILLE_PASSWORD:
        exit()
    try:
        asyncio.run(main_manager())
    except KeyboardInterrupt:
        logging.info("Программа остановлена пользователем.")
