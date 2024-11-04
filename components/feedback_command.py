from telegram import Update
from telegram.ext import CallbackContext
import datetime

async def feedback_command(update: Update, context: CallbackContext):
    context.user_data.clear()
    context.user_data["awaiting_feedback"] = True
    await update.message.reply_text("Опишите ваш опыт пользования ботом.")


async def handle_feedback(update: Update, context: CallbackContext):
    if context.user_data.get("awaiting_feedback"):
        feedback_text = update.message.text
        context.user_data["awaiting_feedback"] = False
        save_feedback(feedback_text)
        await update.message.reply_text("Спасибо за отзыв!")
    else:
        await update.message.reply_text("Отправьте команду /feedback для оценивания работы бота")

def save_feedback(feedback_text):
    with open("feedback.txt", "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp}: {feedback_text}\n")
