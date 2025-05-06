import logging
import random
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

MAIN_MENU, DICE_MENU, TIMER_MENU, TIMER_RUNNING = range(4)


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not hasattr(context, 'application') or not hasattr(context.application, 'job_queue'):
        logger.error("Job queue is not accessible via context.application.job_queue in remove_job_if_exists")
        return False
    job_queue = context.application.job_queue
    current_jobs = job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["/dice", "/timer"]]
    await update.message.reply_text(
        "Привет! Я твой помощник для настольных игр. Выбери действие:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, resize_keyboard=True
        ),
    )
    return MAIN_MENU


async def dice_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        ["Кинуть 1 шестигранный кубик (d6)"],
        ["Кинуть 2 шестигранных кубика (2d6)"],
        ["Кинуть 20-гранный кубик (d20)"],
        ["Назад"],
    ]
    await update.message.reply_text(
        "Выбери, какой кубик бросить:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, resize_keyboard=True
        ),
    )
    return DICE_MENU


async def roll_d6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    roll = random.randint(1, 6)
    await update.message.reply_text(f"Выпало: {roll}")
    return DICE_MENU


async def roll_2d6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    await update.message.reply_text(f"Выпало: {roll1} и {roll2} (сумма: {roll1 + roll2})")
    return DICE_MENU


async def roll_d20(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    roll = random.randint(1, 20)
    await update.message.reply_text(f"Выпало: {roll}")
    return DICE_MENU


async def timer_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        ["30 секунд", "1 минута"],
        ["5 минут", "Назад"],
    ]
    await update.message.reply_text(
        "На сколько засечь таймер?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return TIMER_MENU


async def timer_task(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    duration_text = job.data.get("duration_text", "Время")
    await context.bot.send_message(job.chat_id, text=f"{duration_text} истекло!")
    logger.info(f"Таймер для chat_id {job.chat_id} ({duration_text}) истек.")


async def set_custom_timer(update: Update, context: ContextTypes.DEFAULT_TYPE, seconds: int, duration_text: str) -> int:
    chat_id = update.effective_message.chat_id
    remove_job_if_exists(str(chat_id), context)

    if not hasattr(context, 'application') or not hasattr(context.application, 'job_queue'):
        logger.error(f"Не удалось установить таймер для chat_id {chat_id}: job_queue не найден.")
        await update.effective_message.reply_text("Ошибка: не удалось получить доступ к очереди задач.")
        return TIMER_MENU

    job_queue = context.application.job_queue
    job_queue.run_once(timer_task, seconds, chat_id=chat_id, name=str(chat_id), data={"duration_text": duration_text})

    await update.message.reply_text(
        f"Засек {duration_text}.",
        reply_markup=ReplyKeyboardMarkup([["/close_timer"]], resize_keyboard=True, one_time_keyboard=False),
    )
    logger.info(f"Таймер установлен для chat_id {chat_id} на {duration_text} ({seconds} сек).")
    return TIMER_RUNNING


async def timer_30_sec(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await set_custom_timer(update, context, 30, "30 секунд")


async def timer_1_min(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await set_custom_timer(update, context, 60, "1 минута")


async def timer_5_min(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await set_custom_timer(update, context, 300, "5 минут")


async def close_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Таймер сброшен." if job_removed else "Активных таймеров для сброса нет."
    await update.message.reply_text(text)
    logger.info(f"Попытка сброса таймера для chat_id {chat_id}. Результат: {text}")
    return await start(update, context)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Действие отменено. Чтобы начать заново, введите /start.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    if BOT_TOKEN == "YOUR_ACTUAL_BOT_TOKEN" or not BOT_TOKEN:
        logger.error("Пожалуйста, установите корректный BOT_TOKEN.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CommandHandler("dice", dice_menu),
                MessageHandler(filters.Regex(r"^/dice$"), dice_menu),
                CommandHandler("timer", timer_menu),
                MessageHandler(filters.Regex(r"^/timer$"), timer_menu),
            ],
            DICE_MENU: [
                MessageHandler(filters.Regex(r"^Кинуть 1 шестигранный кубик \(d6\)$"), roll_d6),
                MessageHandler(filters.Regex(r"^Кинуть 2 шестигранных кубика \(2d6\)$"), roll_2d6),
                MessageHandler(filters.Regex(r"^Кинуть 20-гранный кубик \(d20\)$"), roll_d20),
                MessageHandler(filters.Regex(r"^Назад$"), start),
                CommandHandler("start", start),
            ],
            TIMER_MENU: [
                MessageHandler(filters.Regex(r"^30 секунд$"), timer_30_sec),
                MessageHandler(filters.Regex(r"^1 минута$"), timer_1_min),
                MessageHandler(filters.Regex(r"^5 минут$"), timer_5_min),
                MessageHandler(filters.Regex(r"^Назад$"), start),
                CommandHandler("start", start),
            ],
            TIMER_RUNNING: [
                CommandHandler("close_timer", close_timer),
                MessageHandler(filters.Regex(r"^/close_timer$"), close_timer),
                CommandHandler("start", start),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
        per_message=False
    )

    application.add_handler(conv_handler)

    logger.info("Бот-помощник для настольных игр запускается...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Бот остановлен.")


if __name__ == "__main__":
    main()
