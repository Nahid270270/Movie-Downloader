import os
import logging
import requests
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Env variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
SHORTENER_API_BASE_URL = os.getenv("SHORTENER_API_BASE_URL")  # eg: https://short-link-api.com/api
SHORTENER_API_KEY = os.getenv("SHORTENER_API_KEY")  # API key

# Flask app
flask_app = Flask(__name__)

# Telegram Application
application = Application.builder().token(BOT_TOKEN).build()

# Shorten URL
def shorten_link(url: str) -> str:
    try:
        api_url = f"{SHORTENER_API_BASE_URL}/{SHORTENER_API_KEY}?s={url}"
        res = requests.get(api_url)
        return res.text.strip()
    except Exception as e:
        return url  # fallback

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 স্বাগতম Movie Bot-এ!\n\n"
        "🔎 /latest - নতুন মুভি দেখুন"
    )

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = "The Beekeeper (2024)"
    movie_link = "https://samplemoviepage.com/the-beekeeper"
    short_url = shorten_link(movie_link)
    
    button = [[InlineKeyboardButton("⬇️ Download Now", url=short_url)]]
    await update.message.reply_text(
        f"🎬 {movie_name}\n⭐ IMDb: 7.1/10\n\n⬇️ নিচে থেকে দেখুন বা ডাউনলোড করুন:",
        reply_markup=InlineKeyboardMarkup(button)
    )

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("latest", latest))

# Webhook route
@flask_app.post(f"/{BOT_TOKEN}")
async def webhook():
    data = request.get_json(force=True)
    logging.info(f"Received Update: {data}")
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "OK"

# Health check route
@flask_app.route("/")
def home():
    return "✅ Movie Bot is Running"

# Run app
if __name__ == "__main__":
    import asyncio
    PORT = int(os.environ.get("PORT", 5000))
    WEBHOOK_URL = f"https://your-app-name.onrender.com/{BOT_TOKEN}"  # Replace with your actual Render URL

    async def main():
        await application.bot.set_webhook(WEBHOOK_URL)
        flask_app.run(host="0.0.0.0", port=PORT)

    asyncio.run(main())
