from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_KEY
from components.start_command import start
from components.convert_command import convert
from components.analyze_command import analyze
from components.calculate_fluence import fluence_command, handle_fluence_data
from components.feedback_command import feedback_command, handle_feedback

def main():
    application = Application.builder().token(TELEGRAM_KEY).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("convert", convert))
    application.add_handler(CommandHandler("analyze", analyze))
    application.add_handler(CommandHandler("fluence", fluence_command))
    application.add_handler(CommandHandler("feedback", feedback_command))

    application.add_handler(MessageHandler(filters.Document.FileExtension("txt"), analyze))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот запущен...")
    application.run_polling()

async def handle_text(update, context):
    if context.user_data.get("awaiting_feedback"):
        await handle_feedback(update, context)
    elif context.user_data.get("awaiting_fluence_data"):
        await handle_fluence_data(update, context)
    else:
        await update.message.reply_text("Отправьте команду для начала работы.")

if __name__ == '__main__':
    main()