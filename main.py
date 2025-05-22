import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import os

# ENV variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
SOURCE_CHANNEL = -1001234567890  # তোমার চ্যানেল ID

# Clients
bot = Client("movie-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
user = Client("user-session", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# Search Handler
@bot.on_message(filters.private | filters.group & filters.text)
async def search_movie(bot: Client, message: Message):
    query = message.text.strip()
    if not query:
        return await message.reply("দয়া করে একটি সিনেমার নাম লিখুন।")

    results = []
    try:
        async for msg in user.search_messages(chat_id=SOURCE_CHANNEL, query=query, limit=5):
            if msg.text or msg.caption:
                results.append(msg)

        if not results:
            return await message.reply("দুঃখিত, কিছুই পাওয়া যায়নি।")

        for msg in results:
            sent = await msg.copy(chat_id=message.chat.id)
            await asyncio.sleep(1)
            await asyncio.create_task(delete_after(sent, 300))

    except Exception as e:
        await message.reply(f"এরর: {e}")

# Auto delete function
async def delete_after(msg: Message, delay: int):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except:
        pass

# Run both clients
async def main():
    await user.start()
    await bot.start()
    print("Bot is running...")
    await idle()
    await user.stop()
    await bot.stop()

from pyrogram.idle import idle
asyncio.run(main())
