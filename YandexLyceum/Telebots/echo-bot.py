import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler

BOT_TOKEN = "7837219498:AAE-KLppZJQlv4u2tIgyVBENT6Fi-JEFw3A"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def echo(update, context):
    received_text = update.message.text
    reply_message = f"Я получил сообщение «{received_text}»"
    logger.info(f"User {update.effective_user.id} sent: '{received_text}', Bot replied: '{reply_message}'")
    await update.message.reply_text(reply_message)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напиши мне что-нибудь.",
    )


async def help_command(update, context):
    await update.message.reply_text(
        "Просто отправь мне текстовое сообщение, и я отвечу: 'Я получил сообщение «твое_сообщение»'.")


def main():
    if BOT_TOKEN == "YOUR_ACTUAL_BOT_TOKEN" or not BOT_TOKEN:
        logger.error("Пожалуйста, установите корректный BOT_TOKEN.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(text_handler)

    logger.info("Бот запускается...")
    application.run_polling()
    logger.info("Бот остановлен.")


if __name__ == '__main__':
    main()
