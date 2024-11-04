import numpy as np
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import CallbackContext

async def analyze(update: Update, context: CallbackContext):
    file = await context.bot.get_file(update.message.document.file_id)
    await file.download_to_drive("spectrum_data.txt")

    wavelengths, intensities = [], []
    with open("spectrum_data.txt", 'r') as f:
        for line in f:
            parts = line.split()
            wavelengths.append(float(parts[0]))
            intensities.append(float(parts[1]))

    wavelengths = np.array(wavelengths)
    intensities = np.array(intensities)

    peak_index = np.argmax(intensities)
    resonance_wavelength = wavelengths[peak_index]

    half_max = intensities[peak_index] / 2
    left_index = np.where(intensities[:peak_index] <= half_max)[0][-1]
    right_index = peak_index + np.where(intensities[peak_index:] <= half_max)[0][0]
    fwhm = wavelengths[right_index] - wavelengths[left_index]

    plt.figure(figsize=(10, 6))
    plt.plot(wavelengths, intensities, label="Спектр")
    plt.axvline(resonance_wavelength, color="red", linestyle="--", label=f"Резонанс: {resonance_wavelength:.2f} нм")
    plt.axhline(half_max, color="green", linestyle="--", label=f"FWHM: {fwhm:.2f} нм")
    plt.fill_between(wavelengths[left_index:right_index], intensities[left_index:right_index], color="green", alpha=0.3)
    plt.xlabel("Длина волны (нм)")
    plt.ylabel("Интенсивность")
    plt.legend()
    plt.title("Анализ спектра")

    plt.savefig("spectrum_analysis.png")
    plt.close()
    with open("spectrum_analysis.png", "rb") as photo:
        await update.message.reply_photo(photo=photo, caption=f"Резонанс: {resonance_wavelength:.2f} нм\nFWHM: {fwhm:.2f} нм")