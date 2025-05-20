import os
import cloudscraper
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client("bdmovie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

scraper = cloudscraper.create_scraper()
BASE_URL = "https://bdmusic99.asia"

def search_movie(movie_name):
    search_url = f"{BASE_URL}/?s={movie_name.replace(' ', '+')}"
    res = scraper.get(search_url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    posts = soup.select("h2.entry-title a")
    if not posts:
        return None, None
    return posts[0]['href'], posts[0].text.strip()

def get_download_links(post_url):
    res = scraper.get(post_url, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href']
        text = a_tag.get_text(strip=True)
        if href.startswith("http") and any(x in href for x in ["mediafire", "drive", "gdtot", "mega", "bdmusic"]):
            links.append(f"{text} ➤ {href}")
    return links

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("স্বাগতম! মুভির নাম দিন, আমি ডাউনলোড লিংক বের করে দেব। উদাহরণ: `Kabuliwala`")

@bot.on_message(filters.text & ~filters.command("start"))
async def movie_search(client, message: Message):
    movie_name = message.text.strip()
    await message.reply("অনুগ্রহ করে অপেক্ষা করুন...")
    post_url, title = search_movie(movie_name)
    if not post_url:
        await message.reply("দুঃখিত, মুভি পাওয়া যায়নি।")
        return
    links = get_download_links(post_url)
    if not links:
        await message.reply("ডাউনলোড লিংক পাওয়া যায়নি।")
        return
    text = f"**{title}** এর ডাউনলোড লিংক:\n\n" + "\n".join(links)
    await message.reply(text, disable_web_page_preview=True)

if __name__ == "__main__":
    bot.run()
