import logging
import datetime
from telegram.ext import Application, MessageHandler, filters, CommandHandler

BOT_TOKEN = "7837219498:AAE-KLppZJQlv4u2tIgyVBENT6Fi-JEFw3A"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот с командами /time и /date. Напиши мне что-нибудь, и я пришлю это назад!",
    )


async def help_command(update, context):
    await update.message.reply_text(
        "Доступные команды:\n/start - начало работы\n/help - эта справка\n/time - показать текущее время\n/date - показать текущую дату\n\nТакже я отвечаю на обычные текстовые сообщения: 'Я получил сообщение «ваше_сообщение»'")


async def echo(update, context):
    received_text = update.message.text
    reply_message = f"Я получил сообщение «{received_text}»"
    logger.info(f"User {update.effective_user.id} sent text: '{received_text}', Bot replied: '{reply_message}'")
    await update.message.reply_text(reply_message)


async def time_command(update, context):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    logger.info(f"User {update.effective_user.id} requested /time. Current time: {current_time}")
    await update.message.reply_text(f"Текущее время: {current_time}")


async def date_command(update, context):
    today = datetime.date.today()
    current_date = today.strftime("%d.%m.%Y")
    logger.info(f"User {update.effective_user.id} requested /date. Current date: {current_date}")
    await update.message.reply_text(f"Сегодняшняя дата: {current_date}")


def main():
    if BOT_TOKEN == "YOUR_ACTUAL_BOT_TOKEN" or not BOT_TOKEN:
        logger.error("Пожалуйста, установите корректный BOT_TOKEN.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("date", date_command))

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(text_handler)

    logger.info("Бот запускается...")
    application.run_polling()
    logger.info("Бот остановлен.")


if __name__ == '__main__':
    main()
