from pyrogram import Client, filters
import asyncio

API_ID = 123456  # তোমার api_id
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
SESSION_STRING = "your_user_session"
SOURCE_CHANNEL = -100xxxxxxxxxx  # চ্যানেল ID

bot = Client("movie-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
user = Client("user", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)


@bot.on_message(filters.private | filters.group & filters.text)
async def search_movie(client, message):
    query = message.text.strip()
    results = []
    async for msg in user.search_messages(SOURCE_CHANNEL, query, limit=5):
        results.append(msg)

    if not results:
        await message.reply("কোনও কিছু পাওয়া যায়নি।")
        return

    for msg in results:
        sent = await msg.copy(chat_id=message.chat.id)
        await asyncio.sleep(300)
        await sent.delete()


async def main():
    await user.start()
    await bot.start()
    print("Bot is running...")
    await idle()
    await bot.stop()
    await user.stop()

from pyrogram.idle import idle
asyncio.run(main())
