import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHORTENER_API_KEY = os.getenv("SHORTENER_API_KEY")

def shorten_link(url):
    # এখানে আপনার শর্টনার API এর রিকোয়েস্ট পাঠাবেন
    api_url = f"https://ouo.io/api/{SHORTENER_API_KEY}?s={url}"
    res = requests.get(api_url)
    return res.text.strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Movie Bot এ স্বাগতম!\n\n"
        "🔍 /search <মুভির নাম>\n"
        "🔥 /latest – নতুন মুভি দেখুন"
    )

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = "The Beekeeper (2024)"
    movie_url = "https://samplemoviesite.com/beekeeper"
    short_url = shorten_link(movie_url)
    
    buttons = [[InlineKeyboardButton("Download Now", url=short_url)]]
    await update.message.reply_text(
        f"🎬 {movie_name}\n⭐ 7.1/10\n⬇️ Watch or Download নিচে:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("latest", latest))

if __name__ == '__main__':
    app.run_polling()
