import os
import requests
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Environment Variables থেকে নিচ্ছি
BOT_TOKEN = os.getenv("BOT_TOKEN")
SHORTENER_API_BASE_URL = os.getenv("SHORTENER_API_BASE_URL")  # যেমন: https://api.shortener.com
SHORTENER_API_KEY = os.getenv("SHORTENER_API_KEY")            # আপনার API key

# Flask অ্যাপ
flask_app = Flask(__name__)

# Telegram বট অ্যাপ্লিকেশন
application = Application.builder().token(BOT_TOKEN).build()

# লিংক শর্টেন করার ফাংশন
def shorten_link(original_url):
    try:
        api_url = f"{SHORTENER_API_BASE_URL}/{SHORTENER_API_KEY}?s={original_url}"
        response = requests.get(api_url)
        return response.text.strip()
    except Exception as e:
        return f"Error shortening link: {e}"

# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Movie Bot এ স্বাগতম!\n\n"
        "🔍 /search <মুভির নাম>\n"
        "🔥 /latest – নতুন মুভি দেখুন"
    )

# /latest কমান্ড হ্যান্ডলার
async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = "The Beekeeper (2024)"
    movie_url = "https://samplemoviesite.com/beekeeper"  # আসল মুভি URL এখানে বসাবেন
    short_url = shorten_link(movie_url)

    buttons = [[InlineKeyboardButton("⬇️ Download Now", url=short_url)]]

    await update.message.reply_text(
        f"🎬 {movie_name}\n⭐ 7.1/10\n⬇️ Watch or Download নিচে:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# হ্যান্ডলারগুলো অ্যাড করা হচ্ছে
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("latest", latest))

# Telegram webhook route
@flask_app.post(f"/{BOT_TOKEN}")
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# হোম পেজ
@flask_app.route("/")
def home():
    return "Movie Bot is Running"

# রানার ফাংশন
if __name__ == "__main__":
    import asyncio
    PORT = int(os.environ.get("PORT", 5000))
    WEBHOOK_URL = f"https://movie-downloader-21cp.onrender.com/"8124429702:AAGN2Wk9_R3F_tgArbgsJRj5M3u4HRjs6nE"  # আপনার Render URL ও টোকেন অনুযায়ী পরিবর্তন করুন

    async def main():
        await application.bot.set_webhook(WEBHOOK_URL)
        flask_app.run(host="0.0.0.0", port=PORT)

    asyncio.run(main())
