import os
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)
bot = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

headers = {"User-Agent": "Mozilla/5.0"}

# Helper: Extract download links from post page
def extract_links(post_url):
    try:
        res = requests.get(post_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            # Filter known file hosting domains or direct links
            if any(domain in href for domain in ["gdtot.com", "drive.google.com", "mega.nz", "mediafire.com", "gofile.io", "pixeldrain.com", "onedrive.live.com", "direct", "bit.ly", "tinyurl.com"]):
                links.append(f"{text}: {href}")
        return links
    except Exception as e:
        return []

# Site-specific search functions
def search_site(base_url, query):
    try:
        search_url = f"{base_url}/?s=" + query.replace(" ", "+")
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        first_post = soup.select_one("h2.entry-title a")
        if not first_post:
            return None, None
        title = first_post.text.strip()
        post_url = first_post["href"]
        links = extract_links(post_url)
        return title, links
    except Exception as e:
        return None, None

# Master search over multiple sites in order
def master_search(query):
    sites = [
        "https://mlsbd.shop",
        "https://moviesmod.us",
        "https://vegamovies.team",
        "https://9xmovies.sbs",
    ]
    for site in sites:
        title, links = search_site(site, query)
        if title and links:
            return title, links
    return None, None

# Bot commands
@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("Hi! Send me a movie name and I'll find download links for you from popular sites.")

@bot.on_message(filters.text & ~filters.command("start"))
async def search_movie(client, message: Message):
    query = message.text.strip()
    await message.reply("Searching for your movie, please wait...")
    title, links = master_search(query)
    if not title or not links:
        await message.reply("Sorry, no results found for your query.")
        return
    response = f"**{title}**\n\n"
    for link in links:
        response += f"{link}\n"
    await message.reply(response, disable_web_page_preview=True)

@app.route('/')
def home():
    return "Movie Bot is Running!"

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.run()
