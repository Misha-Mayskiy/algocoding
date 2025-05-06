import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
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

ENTRANCE_HALL, HALL_1, HALL_2, HALL_3, HALL_4 = range(5)

DESCRIPTIONS = {
    "entrance": "Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!",
    "hall1": "В Зале 1 представлена экспозиция древнего мира. Здесь вы увидите артефакты возрастом более 5000 лет.",
    "hall2": "Зал 2 посвящен эпохе Средневековья. Обратите внимание на рыцарские доспехи и манускрипты.",
    "hall3": "В Зале 3 вы окунетесь в эпоху Возрождения. Картины великих мастеров и скульптуры ждут вас.",
    "hall4": "Зал 4 представляет современное искусство. Здесь собраны работы художников XX и XXI веков.",
    "exit": "Всего доброго, не забудьте забрать верхнюю одежду в гардеробе! Ждем вас снова!",
}

KEYBOARDS = {
    ENTRANCE_HALL: [["Войти в Зал 1"]],
    HALL_1: [["Перейти в Зал 2"], ["На выход"]],
    HALL_2: [["Перейти в Зал 3"]],
    HALL_3: [["Перейти в Зал 1", "Перейти в Зал 4"]],
    HALL_4: [["Перейти в Зал 1"]],
}

TRANSITION_PROMPTS = {
    ENTRANCE_HALL: {"Войти в Зал 1": "Вы можете войти в Зал 1 (Древний мир)."},
    HALL_1: {
        "Перейти в Зал 2": "Из этого зала можно пройти в Зал 2 (Средневековье).",
        "На выход": "Или вы можете направиться к выходу из музея."
    },
    HALL_2: {"Перейти в Зал 3": "Далее по маршруту Зал 3 (Эпоха Возрождения)."},
    HALL_3: {
        "Перейти в Зал 1": "Можно вернуться в Зал 1 (Древний мир).",
        "Перейти в Зал 4": "Или посетить Зал 4 (Современное искусство)."
    },
    HALL_4: {"Перейти в Зал 1": "Из этого зала можно вернуться в Зал 1 (Древний мир)."},
}


async def send_location_info(update: Update, current_state_key: int, description_key: str):
    description = DESCRIPTIONS[description_key]
    keyboard_layout = KEYBOARDS.get(current_state_key)

    possible_moves_texts = []
    if current_state_key in TRANSITION_PROMPTS:
        for move_description in TRANSITION_PROMPTS[current_state_key].values():
            possible_moves_texts.append(f"- {move_description}")

    message_text = description
    if possible_moves_texts:
        message_text += "\n\nКуда направимся дальше?\n" + "\n".join(possible_moves_texts)

    reply_markup = ReplyKeyboardMarkup(keyboard_layout, resize_keyboard=True,
                                       one_time_keyboard=True) if keyboard_layout else ReplyKeyboardRemove()

    await update.message.reply_text(message_text, reply_markup=reply_markup)


async def start_excursion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"User {update.effective_user.id} started the museum tour.")
    await send_location_info(update, ENTRANCE_HALL, "entrance")
    return ENTRANCE_HALL


async def go_to_hall_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"User {update.effective_user.id} in Hall 1.")
    await send_location_info(update, HALL_1, "hall1")
    return HALL_1


async def go_to_hall_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"User {update.effective_user.id} in Hall 2.")
    await send_location_info(update, HALL_2, "hall2")
    return HALL_2


async def go_to_hall_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"User {update.effective_user.id} in Hall 3.")
    await send_location_info(update, HALL_3, "hall3")
    return HALL_3


async def go_to_hall_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"User {update.effective_user.id} in Hall 4.")
    await send_location_info(update, HALL_4, "hall4")
    return HALL_4


async def go_to_exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"User {update.effective_user.id} is exiting the museum.")
    await update.message.reply_text(DESCRIPTIONS["exit"], reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def cancel_tour(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Экскурсия прервана. Чтобы начать заново, введите /start.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    if BOT_TOKEN == "YOUR_ACTUAL_BOT_TOKEN" or not BOT_TOKEN:
        logger.error("Пожалуйста, установите корректный BOT_TOKEN.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_excursion)],
        states={
            ENTRANCE_HALL: [MessageHandler(filters.Regex(r"^Войти в Зал 1$"), go_to_hall_1)],
            HALL_1: [
                MessageHandler(filters.Regex(r"^Перейти в Зал 2$"), go_to_hall_2),
                MessageHandler(filters.Regex(r"^На выход$"), go_to_exit),
            ],
            HALL_2: [MessageHandler(filters.Regex(r"^Перейти в Зал 3$"), go_to_hall_3)],
            HALL_3: [
                MessageHandler(filters.Regex(r"^Перейти в Зал 1$"), go_to_hall_1),
                MessageHandler(filters.Regex(r"^Перейти в Зал 4$"), go_to_hall_4),
            ],
            HALL_4: [MessageHandler(filters.Regex(r"^Перейти в Зал 1$"), go_to_hall_1)],
        },
        fallbacks=[CommandHandler("cancel", cancel_tour), CommandHandler("start", start_excursion)],
        per_message=False,
    )

    application.add_handler(conv_handler)

    logger.info("Бот-экскурсовод запускается...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Бот остановлен.")


if __name__ == "__main__":
    main()
