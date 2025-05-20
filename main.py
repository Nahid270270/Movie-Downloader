import os
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_mlsbd_links(movie_name):
    search_url = f"https://mlsbd.shop/?s={movie_name.replace(' ', '+')}"
    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        post = soup.select_one("h2.entry-title a")
        if not post:
            return None, None
        post_url = post['href']
        post_title = post.text.strip()

        # এখন পোস্ট পেজ থেকে ডাউনলোড লিংক বের করব
        post_res = requests.get(post_url, headers=headers, timeout=10)
        post_soup = BeautifulSoup(post_res.text, "html.parser")

        links = []
        # ডাউনলোড লিংকগুলো সাধারণত <a> ট্যাগে থাকে যাদের href গুলো ডাউনলোড লিংক
        for a_tag in post_soup.find_all("a", href=True):
            href = a_tag['href']
            text = a_tag.get_text(strip=True)
            if href.startswith("http") and any(x in href for x in ["gdtot", "drive.google.com", "mega.nz", "mediafire.com", "mlsbd.shop"]):
                links.append(f"{text} -> {href}")

        if not links:
            # যদি ডাউনলোড লিংক না পাওয়া যায় তবে সাইটের অন্য যেকোনো লিংক দিতে পারেন
            for a_tag in post_soup.find_all("a", href=True):
                href = a_tag['href']
                text = a_tag.get_text(strip=True)
                if href.startswith("http"):
                    links.append(f"{text} -> {href}")

        return post_title, links
    except Exception as e:
        print(f"Error: {e}")
        return None, None

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("হ্যালো! মুভির নাম পাঠান, আমি আপনাকে ডাউনলোড লিংক দিয়ে দিবো।")

@bot.on_message(filters.text & ~filters.command("start"))
async def search_movie(client, message: Message):
    movie_name = message.text.strip()
    await message.reply("মুভি খুঁজছি, একটু অপেক্ষা করুন...")
    title, links = get_mlsbd_links(movie_name)
    if not title or not links:
        await message.reply("দুঃখিত, মুভি পাওয়া যায়নি। অন্য নাম দিয়ে আবার চেষ্টা করুন।")
        return
    response = f"**{title}** এর ডাউনলোড লিংক:\n\n"
    for link in links:
        response += f"{link}\n"
    await message.reply(response, disable_web_page_preview=True)

if __name__ == "__main__":
    bot.run()
