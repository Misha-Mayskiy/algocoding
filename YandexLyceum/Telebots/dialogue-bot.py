import logging
from telegram import Update, ReplyKeyboardRemove
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

ASK_CITY, ASK_WEATHER_WITH_CITY, ASK_WEATHER_NO_CITY = range(3)


async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "Вы можете пропустить вопрос о городе, послав команду /skip.\n\n"
        "В каком городе вы живёте?"
    )
    return ASK_CITY


async def city_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    locality = update.message.text
    context.user_data['locality'] = locality
    logger.info(f"User {update.effective_user.first_name} lives in: {locality}")
    await update.message.reply_text(
        f"Какая погода в городе {locality}?"
    )
    return ASK_WEATHER_WITH_CITY


async def skip_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"User {update.effective_user.first_name} skipped the city question.")
    context.user_data.pop('locality', None)
    await update.message.reply_text(
        "Хорошо, пропустим город. Какая погода у вас за окном?"
    )
    return ASK_WEATHER_NO_CITY


async def weather_response_with_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    weather = update.message.text
    locality = context.user_data.get('locality', 'вашем городе')
    logger.info(f"Weather in {locality}: {weather}")
    await update.message.reply_text(
        f"Спасибо за участие в опросе! Надеюсь, погода в городе {locality} хорошая!"
    )
    context.user_data.clear()
    return ConversationHandler.END


async def weather_response_no_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    weather = update.message.text
    logger.info(f"Weather (city skipped): {weather}")
    await update.message.reply_text(
        f"Спасибо за участие в опросе! Надеюсь, погода у вас за окном хорошая!"
    )
    context.user_data.clear()
    return ConversationHandler.END


async def stop_survey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the survey.", user.first_name)
    await update.message.reply_text(
        "Опрос прерван. Всего доброго!", reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END


def main() -> None:
    if BOT_TOKEN == "YOUR_ACTUAL_BOT_TOKEN" or not BOT_TOKEN:
        logger.error("Пожалуйста, установите корректный BOT_TOKEN.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_survey)],
        states={
            ASK_CITY: [
                CommandHandler("skip", skip_city),
                MessageHandler(filters.TEXT & ~filters.COMMAND, city_response),
            ],
            ASK_WEATHER_WITH_CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, weather_response_with_city),
            ],
            ASK_WEATHER_NO_CITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, weather_response_no_city),
            ],
        },
        fallbacks=[CommandHandler("stop", stop_survey)],
    )

    application.add_handler(conv_handler)

    logger.info("Бот для опроса запускается...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Бот остановлен.")


if __name__ == "__main__":
    main()
