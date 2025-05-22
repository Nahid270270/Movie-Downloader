from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SESSION = os.environ.get("SESSION_STRING")
SOURCE_CHANNEL = os.environ.get("SOURCE_CHANNEL")  # just "channelusername" (no @)
AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", 300))

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)


@bot.on_message(filters.private | filters.group & filters.text)
async def search_movie(bot_client, message: Message):
    query = message.text

    await message.reply_text("Searching...", quote=True)
    results = []

    async with user:
        async for msg in user.search_messages(SOURCE_CHANNEL, query, limit=5):
            results.append(msg)

    if not results:
        return await message.reply_text("No results found.")

    for msg in results:
        sent = await msg.copy(chat_id=message.chat.id)
        await asyncio.sleep(2)
        await asyncio.create_task(auto_delete(sent))


async def auto_delete(msg: Message):
    await asyncio.sleep(AUTO_DELETE_TIME)
    try:
        await msg.delete()
    except:
        pass


if __name__ == "__main__":
    user.start()  # start user client first
    bot.run()
