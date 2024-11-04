from telegram import Update
from telegram.ext import CallbackContext

def calculate_fluence(power: float, pulse_duration: float, spot_area: float):
    return (power * pulse_duration) / spot_area

async def fluence_command(update: Update, context: CallbackContext):
    context.user_data.clear()
    context.user_data["awaiting_fluence_data"] = True
    await update.message.reply_text("Введите параметры для расчета флюенса (мощность, длительность импульса, площадь):\nПример: 5, 0.0001, 0.002")


async def handle_fluence_data(update: Update, context: CallbackContext):
    if context.user_data.get("awaiting_fluence_data"):
        user_input = update.message.text.split(",")

        if len(user_input) != 3:
            await update.message.reply_text("Ошибка: введенные данные некоректны. Введдите три параметра через запятую(1, 1, 1)")
            return

        try:
            power, pulse_duration, spot_area = map(float, update.message.text.split(","))
            fluence = calculate_fluence(power, pulse_duration, spot_area)
            await update.message.reply_text(f"Флюенс лазера составляет: {fluence:.2f} Дж/м²")
        except ValueError:
            await update.message.reply_text("Ошибка ввода. Введите три числовых параметра, разделенных запятыми.")
        context.user_data["awaiting_fluence_data"] = False
