import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")  # example: -1001234567890
DELETE_TIME = 300  # 5 minutes

app = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
flask_app = Flask(__name__)


@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply_text("স্বাগতম! আপনি যেকোনো মুভির নাম লিখে সার্চ করতে পারেন।")


@app.on_message(filters.command("help"))
async def help_handler(client, message: Message):
    await message.reply_text("এই বট দিয়ে আপনি আপনার চ্যানেল থেকে মুভি খুঁজতে পারবেন। শুধু মুভির নাম লিখুন।")


@app.on_message(filters.text & ~filters.command(["start", "help"]))
async def search_movie(client, message: Message):
    query = message.text.lower()
    results = []

    async for msg in client.search_messages(SOURCE_CHANNEL, query):
        if msg.video or msg.document or msg.text:
            results.append(msg)

    if not results:
        sent = await message.reply_text("কোনো মুভি পাওয়া যায়নি। আবার চেষ্টা করুন।")
        await asyncio.sleep(DELETE_TIME)
        await sent.delete()
        return

    for msg in results[:5]:
        sent = await msg.copy(chat_id=message.chat.id)
        await asyncio.sleep(DELETE_TIME)
        try:
            await sent.delete()
        except:
            pass


@flask_app.route("/")
def home():
    return "Bot is running!"


def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


def start_bot():
    app.run()


if __name__ == "__main__":
    Thread(target=run_flask).start()
    start_bot()
