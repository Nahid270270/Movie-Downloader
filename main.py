import os
import requests
from bs4 import BeautifulSoup
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message
import threading

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
bot = Client("movie-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

BASE_URL = "https://moviesmod.dev"

def search_moviesmod(query):
    search_url = f"{BASE_URL}/?s=" + query.replace(" ", "+")
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for post in soup.select(".ml-item")[:3]:
        title = post.select_one(".mli-info h2").get_text(strip=True)
        link = post.select_one("a")['href']
        results.append((title, link))
    return results

def get_download_links(post_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(post_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    links = []
    for a in soup.select("a[href^='http']"):
        href = a['href']
        text = a.get_text(strip=True)
        if any(x in href for x in [".gd", "mediafire", "drive", "app"]):
            links.append(f"{text}: {href}")
    return links[:5]

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("Welcome! Send me a movie name and I'll give you the direct download links.")

@bot.on_message(filters.text & ~filters.command("start"))
async def movie_search(client, message: Message):
    query = message.text
    results = search_moviesmod(query)
    if not results:
        await message.reply("No results found.")
        return

    reply_text = ""
    for title, link in results:
        reply_text += f"🎬 **{title}**\n"
        dl_links = get_download_links(link)
        for l in dl_links:
            reply_text += f"{l}\n"
        reply_text += "\n"

    await message.reply(reply_text, disable_web_page_preview=True)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    # Flask ও Pyrogram একসাথে চালানোর জন্য Thread ব্যবহার করছি
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.run()
