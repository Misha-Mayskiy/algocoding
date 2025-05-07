import logging
import json
import asyncio
import aiohttp
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = "7837219498:AAE-KLppZJQlv4u2tIgyVBENT6Fi-JEFw3A"
YANDEX_GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
GEOCODER_API_URL = "http://geocode-maps.yandex.ru/1.x/"
STATIC_MAPS_API_URL = "https://static-maps.yandex.ru/1.x/"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение."""
    await update.message.reply_text(
        "Привет! Я бот-геокодер. Отправь мне название места или адрес, "
        "и я постараюсь показать его на карте с меткой."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет инструкцию по использованию."""
    await update.message.reply_text(
        "Просто отправь мне текстовое сообщение с названием объекта или адресом. "
        "Например: 'Красная площадь, Москва' или 'Эйфелева башня'."
    )


async def get_coordinates(session: aiohttp.ClientSession, address: str) -> tuple | None:
    """Получает координаты (долгота, широта) и полное название объекта по адресу."""
    params = {
        "apikey": YANDEX_GEOCODER_API_KEY,
        "geocode": address,
        "format": "json",
        "results": 1
    }
    try:
        async with session.get(GEOCODER_API_URL, params=params) as response:
            response.raise_for_status()
            data = await response.json()

            if not data["response"]["GeoObjectCollection"]["featureMember"]:
                logger.info(f"Геокодер не нашел объектов для запроса: {address}")
                return None, None

            geo_object = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            point_str = geo_object["Point"]["pos"]
            full_address = geo_object["metaDataProperty"]["GeocoderMetaData"]["text"]

            lon, lat = map(float, point_str.split())
            logger.info(f"Координаты для '{address}': lon={lon}, lat={lat}. Полный адрес: {full_address}")
            return (lon, lat), full_address

    except aiohttp.ClientResponseError as http_err:
        logger.error(f"HTTP ошибка при запросе к Геокодеру: {http_err.status} {http_err.message} для {address}")
        raise
    except aiohttp.ClientError as client_err:
        logger.error(f"Ошибка клиента aiohttp при запросе к Геокодеру: {client_err} для {address}")
        raise
    except (KeyError, IndexError, ValueError) as parse_err:
        logger.error(
            f"Ошибка разбора ответа от Геокодера для '{address}': {parse_err}. Ответ: {data if 'data' in locals() else 'нет данных'}")
        return None, None
    except Exception as e:
        logger.error(f"Непредвиденная ошибка в get_coordinates для '{address}': {e}")
        raise


async def handle_location_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    chat_id = update.message.chat_id
    logger.info(f"Получен запрос от user {chat_id}: '{user_text}'")

    if not YANDEX_GEOCODER_API_KEY or YANDEX_GEOCODER_API_KEY == "YOUR_YANDEX_GEOCODER_API_KEY":
        await update.message.reply_text("Ошибка конфигурации: API-ключ Яндекс.Геокодера не установлен.")
        return

    async with aiohttp.ClientSession() as session:
        try:
            coords, full_address = await get_coordinates(session, user_text)

            if coords and full_address:
                lon, lat = coords
                map_params = {
                    "ll": f"{lon},{lat}",
                    "l": "map",
                    "z": "15",
                    "size": "600,450",
                    "pt": f"{lon},{lat},pm2rdm"
                }

                map_request_params_str = "&".join([f"{k}={v}" for k, v in map_params.items()])
                map_request_url = f"{STATIC_MAPS_API_URL}?{map_request_params_str}"

                logger.info(f"Запрос к Static Maps API: {map_request_url}")
                caption_text = f"Нашёл: {full_address}"

                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=map_request_url,
                    caption=caption_text,
                )
            else:
                await update.message.reply_text(
                    f"К сожалению, не удалось найти информацию по вашему запросу: '{user_text}'. "
                    "Попробуйте уточнить запрос или использовать другой."
                )

        except aiohttp.ClientResponseError as http_err:
            error_message = f"Произошла сетевая ошибка при обращении к API: {http_err.status}."
            if http_err.status == 403:
                error_message += " Возможно, проблема с API-ключом."
            elif http_err.status == 400:
                error_message += " Некорректный запрос к API."
            await update.message.reply_text(error_message + " Пожалуйста, попробуйте позже.")
        except aiohttp.ClientError:
            await update.message.reply_text(
                "Произошла ошибка соединения с сервисом карт. Пожалуйста, попробуйте позже.")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка в handle_location_request для '{user_text}': {e}")
            if "Failed to get http url content" in str(e):
                await update.message.reply_text(
                    "Не удалось загрузить карту. Возможно, URL карты недоступен или некорректен. Попробуйте другой запрос."
                )
            else:
                await update.message.reply_text(
                    "Произошла неизвестная ошибка при попытке показать карту. Попробуйте позже.")


def main() -> None:
    """Запускает бота."""
    if BOT_TOKEN == "YOUR_ACTUAL_BOT_TOKEN" or not BOT_TOKEN:
        logger.error("Пожалуйста, установите корректный BOT_TOKEN Telegram бота.")
        return
    if YANDEX_GEOCODER_API_KEY == "YOUR_YANDEX_GEOCODER_API_KEY" or not YANDEX_GEOCODER_API_KEY:
        logger.warning("API-ключ Яндекс.Геокодера не установлен. Функциональность будет ограничена.")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_location_request))

    logger.info("Бот-геокодер запускается...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
