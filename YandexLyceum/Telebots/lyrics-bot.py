import logging
import re
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

BOT_TOKEN = "7837219498:AAE-KLppZJQlv4u2tIgyVBENT6Fi-JEFw3A"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

POEM_LINES = [
    "У лукоморья дуб зелёный",
    "Златая цепь на дубе том:",
    "И днём и ночью кот учёный",
    "Всё ходит по цепи кругом",
    "Идёт направо — песнь заводит,",
    "Налево — сказку говорит.",
    "Там чудеса: там леший бродит,",
    "Русалка на ветвях сидит",
    "Там на неведомых дорожках",
    "Следы невиданных зверей",
    "Избушка там на курьих ножках",
    "Стоит без окон, без дверей",
    "Там лес и дол видений полны",
    "Там о заре прихлынут волны",
    "На брег песчаный и пустой,",
    "И тридцать витязей прекрасных",
    "Чредой из вод выходят ясных,",
    "И с ними дядька их морской",
    "Там королевич мимоходом",
    "Пленяет грозного царя",
    "Там в облаках перед народом",
    "Через леса, через моря",
    "Колдун несёт богатыря",
    "В темнице там царевна тужит,",
    "А бурый волк ей верно служит",
    "Там ступа с Бабою Ягой",
    "Идёт, бредёт сама собой,",
    "Там царь Кащей над златом чахнет",
    "Там русский дух... там Русью пахнет!",
    "И там я был, и мёд я пил",
    "У моря видел дуб зелёный",
    "Под ним сидел, и кот учёный",
    "Свои мне сказки говорил."
]

READING_POEM, AWAITING_RETRY = range(2)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace('ё', 'е')
    text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


async def start_poem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['current_line_index'] = 0
    context.user_data['last_bot_line'] = POEM_LINES[0]
    await update.message.reply_text(f"Давай почитаем стихотворение!\n\nЯ начну:\n{POEM_LINES[0]}")
    logger.info(f"User {update.effective_user.id} started poem. Bot said: {POEM_LINES[0]}")
    context.user_data['expected_line_index'] = 1
    return READING_POEM


async def check_line(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text
    current_expected_index = context.user_data.get('expected_line_index')

    if current_expected_index is None or current_expected_index >= len(POEM_LINES):
        await update.message.reply_text("Что-то пошло не так. Давай начнем сначала? /start")
        return ConversationHandler.END

    expected_line_normalized = normalize_text(POEM_LINES[current_expected_index])
    user_line_normalized = normalize_text(user_text)

    if user_line_normalized == expected_line_normalized:
        logger.info(f"User {update.effective_user.id} correctly said: '{user_text}'")
        next_bot_line_index = current_expected_index + 1
        if next_bot_line_index < len(POEM_LINES):
            bot_reply = POEM_LINES[next_bot_line_index]
            await update.message.reply_text(bot_reply)
            context.user_data['last_bot_line'] = bot_reply
            context.user_data['expected_line_index'] = next_bot_line_index + 1
            return READING_POEM
        else:
            await update.message.reply_text("Отлично! Мы прочитали все стихотворение! 🎉\nХочешь повторить? /start")
            context.user_data.clear()
            return ConversationHandler.END
    else:
        logger.info(
            f"User {update.effective_user.id} made a mistake. Expected: '{POEM_LINES[current_expected_index]}', Got: '{user_text}'")
        reply_keyboard = [['/suphler', '/stop']]
        await update.message.reply_text(
            "Нет, не так... Попробуй еще раз. \nЕсли нужна подсказка, используй /suphler.",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        return AWAITING_RETRY


async def suphler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    current_expected_index = context.user_data.get('expected_line_index')
    if current_expected_index is not None and current_expected_index < len(POEM_LINES):
        expected_line = POEM_LINES[current_expected_index]
        await update.message.reply_text(f"Подсказка: следующая строка должна быть «{expected_line}»")
        logger.info(f"User {update.effective_user.id} used suphler. Hint: {expected_line}")
        reply_keyboard = [['/stop']]
        await update.message.reply_text(
            "Теперь попробуй сказать правильную строку.",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        return AWAITING_RETRY
    else:
        await update.message.reply_text("Сейчас нет строки для подсказки. Может, начнем сначала? /start")
        return ConversationHandler.END


async def stop_poem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s stopped reading the poem.", user.first_name)
    await update.message.reply_text(
        "Чтение прервано. Жаль! Может, в другой раз? /start", reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END


def main() -> None:
    if BOT_TOKEN == "YOUR_ACTUAL_BOT_TOKEN" or not BOT_TOKEN:
        logger.error("Пожалуйста, установите корректный BOT_TOKEN.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_poem)],
        states={
            READING_POEM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, check_line),
            ],
            AWAITING_RETRY: [
                CommandHandler("suphler", suphler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, check_line),
            ]
        },
        fallbacks=[CommandHandler("stop", stop_poem), CommandHandler("start", start_poem)],
        per_message=False,
    )

    application.add_handler(conv_handler)

    logger.info("Бот для чтения стихов запускается...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Бот остановлен.")


if __name__ == "__main__":
    main()
