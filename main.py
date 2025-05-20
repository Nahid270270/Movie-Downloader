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
bot = Client("mlsbd_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

BASE_URL = "https://mlsbd.shop"

def search_mlsbd(query):
    search_url = f"{BASE_URL}/?s=" + query.replace(" ", "+")
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    first_post = soup.select_one("h2.entry-title a")
    if not first_post:
        return None, None
    return first_post.text.strip(), first_post["href"]

def extract_download_links(post_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(post_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if any(x in href for x in ["drive.google", "mega.nz", "mediafire", "gofile", "pixeldrain", "onedrive", "direct"]):
            links.append(f"{text}: {href}")
    return links

@bot.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply("Welcome to MLSBD Movie Bot!\nSend me any movie name to get download links.")

@bot.on_message(filters.text & ~filters.command("start"))
async def handle_query(client, message: Message):
    query = message.text.strip()
    await message.reply("Searching...")
    title, post_url = search_mlsbd(query)
    if not post_url:
        await message.reply("No results found.")
        return

    links = extract_download_links(post_url)
    if not links:
        await message.reply(f"Found **{title}**, but no download links available.")
        return

    response = f"🎬 **{title}**\n\n"
    for link in links:
        response += f"{link}\n"

    await message.reply(response, disable_web_page_preview=True)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.run()
