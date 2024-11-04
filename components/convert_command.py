from telegram import Update
from telegram.ext import ContextTypes
from config import SPEED_OF_LIGHT, PLANCK_CONSTANT, ELECTRON_VOLT, VISIBLE_WAVELENGTH_MIN, VISIBLE_WAVELENGTH_MAX

async def convert(update: Update, context: ContextTypes):
    """
    Переводит частоту и энергию фотона в длину волны и обратно.
    :param <value>: float
    :param <unit>>: str
    :return: str
    """

    if len(context.args) < 2:
        await update.message.reply_text(
            "Ошибка: введите значение и единицу измерения ('lambda', 'frequency' или 'energy').")
        return
    elif len(context.args) > 2:
        await update.message.reply_text(
            "Ошибка: введено более 2 параметров(<value> <unit>")
        return

    value, unit = context.args

    try:
        value = float(value)

        if unit.lower() == 'lambda':
            wavelength = value * 1e-9
            frequency = SPEED_OF_LIGHT / wavelength
            energy = frequency * PLANCK_CONSTANT / ELECTRON_VOLT
            result = (
                f"Длина волны: {value:.2e} нм\n"
                f"Частота: {frequency:.2e} Гц\n"
                f"Энергия: {energy:.2e} эВ\n"
            )
        elif unit.lower() == 'frequency':
            frequency = value
            wavelength = SPEED_OF_LIGHT / frequency
            energy = frequency * PLANCK_CONSTANT / ELECTRON_VOLT
            result = (
                f"Частота: {frequency:.2e} Гц\n"
                f"Длина волны: {wavelength * 1e9:.2e} нм\n"
                f"Энергия: {energy:.2e} эВ\n"
            )
        elif unit.lower() == "energy":
            energy = value * ELECTRON_VOLT
            frequency = energy / PLANCK_CONSTANT
            wavelength = SPEED_OF_LIGHT / frequency
            result = (
                f"Энергия: {value:.2e} эВ\n"
                f"Частота: {frequency:.2e} Гц\n"
                f"Длина волны: {wavelength * 1e9:.2e} нм\n"
            )
        else:
            result = "Неизвестный тип. Пожалуйста, используйте 'lambda', 'frequency' или 'energy'."

        if VISIBLE_WAVELENGTH_MIN <= wavelength <= VISIBLE_WAVELENGTH_MAX:
            result += "\nЭто видимый свет."
        elif wavelength < VISIBLE_WAVELENGTH_MIN:
            result += "\nЭто ультрафиолетовое или более короткое излучение."
        else:
            result += "\nЭто инфракрасное или более длинное излучение."

        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("Ошибка: введите числовое значение для перевода.")
