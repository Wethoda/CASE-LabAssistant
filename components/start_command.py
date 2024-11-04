from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes):
    """
        Сообщение приветсвия
    """

    welcome_mess = (
        "Здравствуйте, я бот LabAssistant, помогу вам в области физики.\n"
        "Мои фунции:\n"
        "1. Перевод частоты и энергии фотона в лину волны и обратно(/convert <value> <unit>.).\n"
        "2. Анализ спектра и поиск резонансов(/analyze и файл.).\n"
        "3. Расчет флюенса лазера по средней мощности(/fluence, бот отправляет пример ввода.).\n"
        "4. Обратная связь о вашем опыте использования(/feedback, а потом пишем отзыв.).\n"
    )


    await update.message.reply_text(welcome_mess)