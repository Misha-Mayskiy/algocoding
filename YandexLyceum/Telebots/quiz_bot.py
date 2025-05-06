import logging
import json
import random
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
QUIZ_FILE = "quiz_data.json"
QUESTIONS_PER_QUIZ = 10
ASKING_QUESTION = range(1)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def load_quiz_data(filename: str) -> list:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if "test" in data and isinstance(data["test"], list):
            return data["test"]
        else:
            logger.error(f"Файл {filename} имеет неверный формат. Отсутствует ключ 'test' или он не является списком.")
            return []
    except FileNotFoundError:
        logger.error(f"Файл с вопросами {filename} не найден.")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле {filename}.")
        return []


ALL_QUESTIONS = load_quiz_data(QUIZ_FILE)


def normalize_answer(text: str) -> str:
    """Приводит ответ к нижнему регистру и удаляет лишние пробелы для сравнения."""
    return text.lower().strip()


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not ALL_QUESTIONS:
        await update.message.reply_text("К сожалению, вопросы для викторины не загружены. Попробуйте позже.")
        return ConversationHandler.END

    if len(ALL_QUESTIONS) < QUESTIONS_PER_QUIZ:
        logger.warning(f"В файле меньше {QUESTIONS_PER_QUIZ} вопросов. Будут использованы все доступные.")
        context.user_data['quiz_questions'] = random.sample(ALL_QUESTIONS, len(ALL_QUESTIONS))
    else:
        context.user_data['quiz_questions'] = random.sample(ALL_QUESTIONS, QUESTIONS_PER_QUIZ)

    context.user_data['current_question_index'] = 0
    context.user_data['score'] = 0

    await update.message.reply_text(
        f"Привет! Начнем викторину из {len(context.user_data['quiz_questions'])} вопросов. Удачи!"
        "\nВы можете прервать викторину командой /stop."
    )
    return await ask_next_question(update, context)


async def ask_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    questions = context.user_data.get('quiz_questions', [])
    current_index = context.user_data.get('current_question_index', 0)

    if current_index < len(questions):
        question_data = questions[current_index]
        context.user_data['current_correct_answer'] = question_data['response']

        await update.message.reply_text(question_data['question'], reply_markup=ReplyKeyboardRemove())
        logger.info(f"User {update.effective_user.id} asking question {current_index + 1}: {question_data['question']}")
        return ASKING_QUESTION
    else:
        score = context.user_data.get('score', 0)
        total_questions = len(questions)
        await update.message.reply_text(
            f"Викторина завершена! Ваш результат: {score} из {total_questions} правильных ответов. 🎉"
            "\nХотите сыграть еще раз? /start",
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data.clear()
        return ConversationHandler.END


async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    correct_answer = context.user_data.get('current_correct_answer')

    normalized_user_answer = normalize_answer(user_answer)
    normalized_correct_answer = normalize_answer(correct_answer)

    if normalized_user_answer == normalized_correct_answer:
        context.user_data['score'] = context.user_data.get('score', 0) + 1
        await update.message.reply_text("Правильно!")
        logger.info(f"User {update.effective_user.id} answered correctly: '{user_answer}'")
    else:
        await update.message.reply_text(f"Неверно. Правильный ответ: {correct_answer}")
        logger.info(
            f"User {update.effective_user.id} answered incorrectly: '{user_answer}'. Correct: '{correct_answer}'")

    context.user_data['current_question_index'] = context.user_data.get('current_question_index', 0) + 1
    return await ask_next_question(update, context)


async def stop_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    score = context.user_data.get('score', 0)
    answered_questions = context.user_data.get('current_question_index', 0)

    logger.info("User %s stopped the quiz.", user.first_name)
    await update.message.reply_text(
        f"Викторина прервана. Ваш текущий счет: {score} из {answered_questions} вопросов."
        "\nЧтобы начать заново, введите /start.",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END


def main() -> None:
    if BOT_TOKEN == "YOUR_ACTUAL_BOT_TOKEN" or not BOT_TOKEN:
        logger.error("Пожалуйста, установите корректный BOT_TOKEN.")
        return
    if not ALL_QUESTIONS:
        logger.error(f"Не удалось загрузить вопросы из {QUIZ_FILE}. Бот не может быть запущен без вопросов.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_quiz)],
        states={
            ASKING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer)],
        },
        fallbacks=[CommandHandler("stop", stop_quiz), CommandHandler("start", start_quiz)],
        per_message=False,
    )

    application.add_handler(conv_handler)

    logger.info("Бот-викторина запускается...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Бот остановлен.")


if __name__ == "__main__":
    main()
