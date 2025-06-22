import telebot
import os
import yt_dlp
import uuid

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    bot.send_message(message.chat.id, "Отправь мне название песни, и я найду и скачаю её для тебя!")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text.strip()
    bot.send_message(message.chat.id, f"🔍 Ищу: {query}...")

    outtmpl = os.path.join(DOWNLOAD_DIR, f"{uuid.uuid4()}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            filename = ydl.prepare_filename(info['entries'][0])
            mp3_file = os.path.splitext(filename)[0] + ".mp3"

        with open(mp3_file, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, title=query)

        os.remove(mp3_file)

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "⚠️ Не удалось найти или скачать песню.")

if __name__ == "__main__":
    bot.infinity_polling()
