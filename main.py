from pyrogram import Client, filters
from pyrogram.types import Message
import os
import asyncio

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION_STRING")
SOURCE_CHANNEL = int(os.environ.get("SOURCE_CHANNEL"))  # like -1001234567890

app = Client(name="movie_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

AUTO_DELETE_TIME = 300  # 5 minutes

@app.on_message(filters.private | filters.group & filters.text & ~filters.edited)
async def search_movie(client: Client, message: Message):
    query = message.text.strip()
    if not query:
        return

    results = []
    async for msg in client.search_messages(SOURCE_CHANNEL, query):
        if msg.text or msg.caption:
            results.append(msg)

    if not results:
        await message.reply("Sorry, movie not found.")
        return

    for msg in results[:5]:
        sent = await msg.copy(message.chat.id)
        await asyncio.sleep(1)
        await asyncio.create_task(auto_delete(sent))

async def auto_delete(msg: Message):
    await asyncio.sleep(AUTO_DELETE_TIME)
    try:
        await msg.delete()
    except:
        pass

app.run()
