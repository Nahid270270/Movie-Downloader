import os
import logging
import requests
from bs4 import BeautifulSoup
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN or not WEBHOOK_URL:
    raise Exception("BOT_TOKEN or WEBHOOK_URL env variable missing!")

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

SEARCH_SITES = [
    "https://1337x.to/search/{query}/1/",
    "https://yts.mx/browse-movies/{query}/all/all/0/latest",
    "https://fmovies.to/search/{query}",
]

def scrape_site(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return []
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        for a in soup.find_all("a", href=True):
            href = a['href']
            text = a.get_text(strip=True) or "Link"
            if "download" in href.lower() or "watch" in href.lower() or "torrent" in href.lower():
                results.append((text, href))
        return results[:5]
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return []

def start(update, context):
    update.message.reply_text(
        "Hi! Use /search followed by movie name to get download/watch links.\nExample: /search Joker"
    )

def search(update, context):
    if not context.args:
        update.message.reply_text("Please provide a movie name.\nUsage: /search Joker")
        return

    query = " ".join(context.args)
    update.message.reply_text(f"Searching links for '{query}'...")

    all_links = []
    for site in SEARCH_SITES:
        url = site.format(query=query.replace(" ", "+"))
        all_links.extend(scrape_site(url))

    if not all_links:
        update.message.reply_text("No download or watch links found for this movie.")
        return

    buttons = [[InlineKeyboardButton(text, url=link)] for text, link in all_links]

    update.message.reply_text(
        "Here are the download/watch links:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("search", search))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/")
def index():
    return "Bot is alive and running."

def set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if status:
        logger.info(f"Webhook set successfully to {WEBHOOK_URL}")
    else:
        logger.error("Failed to set webhook")

if __name__ == "__main__":
    set_webhook()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
