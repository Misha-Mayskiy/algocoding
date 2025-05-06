import logging
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "7837219498:AAE-KLppZJQlv4u2tIgyVBENT6Fi-JEFw3A"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    job_queue = context.application.job_queue
    if not job_queue:
        logger.error("Job queue not found in application context!")
        return False

    current_jobs = job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def task(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    timer_duration = job.data if job.data else "неизвестное количество"
    await context.bot.send_message(job.chat_id, text=f'КУКУ! {timer_duration} сек. прошли!')
    logger.info(f"Таймер для chat_id {job.chat_id} на {timer_duration} сек. сработал.")


async def set_timer(update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    try:
        if not context.args:
            await update.effective_message.reply_text(
                "Пожалуйста, укажите время в секундах после команды.\n"
                "Например: /set_timer 10"
            )
            return

        timer_duration = int(context.args[0])
        if timer_duration <= 0:
            await update.effective_message.reply_text("Время должно быть положительным числом секунд.")
            return
        if timer_duration > 3600:
            await update.effective_message.reply_text("Слишком большое время для таймера (максимум 3600 секунд).")
            return

    except (IndexError, ValueError):
        await update.effective_message.reply_text(
            "Неверный формат времени. Пожалуйста, укажите целое число секунд.\n"
            "Например: /set_timer 10"
        )
        return

    job_removed = remove_job_if_exists(str(chat_id), context)
    job_queue = context.application.job_queue
    if job_queue:
        job_queue.run_once(task, timer_duration, chat_id=chat_id, name=str(chat_id), data=timer_duration)
        text = f'Таймер установлен на {timer_duration} секунд!'
        if job_removed:
            text += ' Предыдущий таймер для этого чата удален.'
        await update.effective_message.reply_text(text)
        logger.info(f"Таймер установлен для chat_id {chat_id} на {timer_duration} секунд.")
    else:
        logger.error(f"Не удалось установить таймер для chat_id {chat_id}: job_queue не найден.")
        await update.effective_message.reply_text("Ошибка: не удалось получить доступ к очереди задач.")


async def unset_timer(update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров.'
    await update.message.reply_text(text)
    logger.info(f"Попытка отмены таймера для chat_id {chat_id}. Результат: {text}")


async def start(update, context):
    await update.message.reply_text(
        "Привет! Я таймер-бот. Используйте команду /set_timer <секунды> для установки таймера."
        "\nНапример: /set_timer 15"
        "\nИспользуйте /unset_timer для отмены."
    )


def main():
    if BOT_TOKEN == "YOUR_ACTUAL_BOT_TOKEN" or not BOT_TOKEN:
        logger.error("Пожалуйста, установите корректный BOT_TOKEN.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_timer", set_timer))
    application.add_handler(CommandHandler("unset_timer", unset_timer))

    logger.info("Бот запускается...")
    application.run_polling()
    logger.info("Бот остановлен.")


if __name__ == '__main__':
    main()
