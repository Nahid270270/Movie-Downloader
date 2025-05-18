import os
import requests
from flask import Flask, request
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, Application

# ENV Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
SHORTENER_API_BASE_URL = os.getenv("SHORTENER_API_BASE_URL")
SHORTENER_API_KEY = os.getenv("SHORTENER_API_KEY")

# Telegram Bot
bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

# Link shortener function
def shorten_link(original_url):
    try:
        api_url = f"{SHORTENER_API_BASE_URL}/{SHORTENER_API_KEY}?s={original_url}"
        response = requests.get(api_url)
        return response.text.strip()
    except Exception as e:
        return f"Error shortening link: {e}"

# Command handlers
async def start(update: Update, context):
    await update.message.reply_text(
        "👋 Movie Bot এ স্বাগতম!\n\n"
        "🔍 /search <মুভির নাম>\n"
        "🔥 /latest – নতুন মুভি দেখুন"
    )

async def latest(update: Update, context):
    movie_name = "The Beekeeper (2024)"
    movie_url = "https://samplemoviesite.com/beekeeper"
    short_url = shorten_link(movie_url)

    buttons = [[InlineKeyboardButton("⬇️ Download Now", url=short_url)]]

    await update.message.reply_text(
        f"🎬 {movie_name}\n⭐ 7.1/10\n⬇️ Watch or Download নিচে:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Telegram dispatcher
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("latest", latest))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put(update)
    return "ok"

@app.route("/")
def index():
    return "Movie Bot is running!"

# Main
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    bot.set_webhook(f"https://your-app-name.onrender.com/{BOT_TOKEN}")  # <-- Replace with your actual URL
    app.run(host="0.0.0.0", port=port)
