import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from googletrans import Translator, LANGUAGES

BOT_TOKEN = "7837219498:AAE-KLppZJQlv4u2tIgyVBENT6Fi-JEFw3A"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING_DIRECTION, TRANSLATING = range(2)
RU_TO_EN = "С русского на английский 🇷🇺➡️🇬🇧"
EN_TO_RU = "С английского на русский 🇬🇧➡️🇷🇺"

translator_instance = None


async def initialize_translator_if_needed():
    """Асинхронно инициализирует глобальный translator_instance."""
    global translator_instance
    if translator_instance is not None:
        try:
            await translator_instance.translate("a", src='en', dest='ru')
            logger.info("Существующий экземпляр Translator работает.")
            return
        except Exception as e:
            logger.warning(f"Существующий экземпляр Translator не работает ({e}). Попытка переинициализации.")
            translator_instance = None

    logger.info("Попытка асинхронной инициализации Googletrans Translator...")
    try:
        temp_translator = Translator()
        test_result = await temp_translator.translate("test", src='en', dest='ru')
        if hasattr(test_result, 'text') and test_result.text:
            translator_instance = temp_translator
            logger.info("Googletrans Translator успешно инициализирован и проверен.")
        else:
            logger.error("Пробный асинхронный перевод не вернул ожидаемый результат (нет текста).")
            translator_instance = None
    except Exception as e:
        logger.error(f"Ошибка асинхронной инициализации Googletrans Translator: {e}.")
        translator_instance = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await initialize_translator_if_needed()

    reply_keyboard = [[RU_TO_EN], [EN_TO_RU]]
    await update.message.reply_text(
        "Привет! Я бот-переводчик. Выбери направление перевода:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return CHOOSING_DIRECTION


async def set_translation_direction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text
    user_id = update.effective_user.id

    if user_choice == RU_TO_EN:
        context.user_data['source_lang'] = 'ru'
        context.user_data['dest_lang'] = 'en'
        chosen_direction_text = "русского на английский"
    elif user_choice == EN_TO_RU:
        context.user_data['source_lang'] = 'en'
        context.user_data['dest_lang'] = 'ru'
        chosen_direction_text = "английского на русский"
    else:
        await update.message.reply_text("Пожалуйста, выбери направление с помощью кнопок.")
        return await start(update, context)  # Возвращаем в начало

    logger.info(f"User {user_id} выбрал направление: {chosen_direction_text}")
    await update.message.reply_text(
        f"Отлично! Теперь я буду переводить с {chosen_direction_text}. "
        "Присылай мне текст для перевода.\n"
        "Чтобы изменить направление, используй команду /start.",
        reply_markup=ReplyKeyboardRemove()
    )
    return TRANSLATING


async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text
    user_id = update.effective_user.id
    source_lang = context.user_data.get('source_lang')
    dest_lang = context.user_data.get('dest_lang')

    if not source_lang or not dest_lang:
        await update.message.reply_text(
            "Направление перевода не установлено. Пожалуйста, начни с команды /start."
        )
        return CHOOSING_DIRECTION

    if translator_instance is None:
        logger.warning("Translator не был инициализирован при старте команды /translate. Попытка инициализировать...")
        await initialize_translator_if_needed()
        if translator_instance is None:
            await update.message.reply_text(
                "Извините, сервис перевода временно недоступен (ошибка инициализации). Попробуйте позже."
            )
            return TRANSLATING

    try:
        translation_result = await translator_instance.translate(user_text, src=source_lang, dest=dest_lang)

        if not hasattr(translation_result, 'text') or not translation_result.text:
            logger.error(f"Результат перевода не имеет атрибута 'text' или текст пуст. Результат: {translation_result}")
            raise AttributeError("Результат перевода не имеет атрибута 'text' или текст пуст")

        translated_text = translation_result.text

        detected_lang_code = translation_result.src if translation_result.src else source_lang
        detected_lang_name = LANGUAGES.get(detected_lang_code.lower(),
                                           detected_lang_code) if detected_lang_code else source_lang

        logger.info(
            f"User {user_id} sent '{user_text}' (detected: {detected_lang_name}). Translated to '{dest_lang}': '{translated_text}'")
        await update.message.reply_text(
            f"Перевод ({detected_lang_name} -> {LANGUAGES.get(dest_lang, dest_lang)}):\n{translated_text}")

    except AttributeError as ae:
        logger.error(f"Ошибка атрибута при переводе для user {user_id}: {ae}")
        await update.message.reply_text(
            "Произошла ошибка при обработке результата перевода. Пожалуйста, попробуйте еще раз позже."
        )
    except Exception as e:
        logger.error(f"Общая ошибка перевода для user {user_id}: {e}\nТекст: {user_text}")
        await initialize_translator_if_needed()
        await update.message.reply_text(
            "Произошла ошибка при переводе. Пожалуйста, попробуйте еще раз позже. Сервис мог быть временно недоступен."
        )

    return TRANSLATING


async def stop_translation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    logger.info(f"User {user_id} stopped translation session.")
    await update.message.reply_text(
        "Сессия перевода завершена. Чтобы начать снова, используй /start.",
        reply_markup=ReplyKeyboardRemove(),
    )
    context.user_data.clear()
    return ConversationHandler.END


def main():
    if BOT_TOKEN == "YOUR_ACTUAL_BOT_TOKEN" or not BOT_TOKEN:
        logger.error("Пожалуйста, установите корректный BOT_TOKEN.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_DIRECTION: [
                MessageHandler(filters.Regex(f"^({RU_TO_EN}|{EN_TO_RU})$"), set_translation_direction),
            ],
            TRANSLATING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text),
                CommandHandler("start", start)
            ],
        },
        fallbacks=[CommandHandler("stop", stop_translation), CommandHandler("start", start)],
        per_message=False,
    )

    application.add_handler(conv_handler)

    logger.info("Бот-переводчик запускается...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Бот остановлен.")


if __name__ == "__main__":
    main()
