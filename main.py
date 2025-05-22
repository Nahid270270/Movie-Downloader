from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_CHANNEL = os.environ.get("SOURCE_CHANNEL")  # username or ID (without @)

app = Client(name="movie-userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)


@app.on_message((filters.private | filters.group) & filters.text)
async def search_movie(client: Client, message: Message):
    query = message.text
    results = []
    async for msg in client.search_messages(SOURCE_CHANNEL, query, limit=5):
        if msg.video or msg.document:
            results.append(msg)

    if not results:
        await message.reply("দুঃখিত, কিছুই পাইনি। সঠিক নাম দিন।")
        return

    for result in results:
        sent = await result.copy(chat_id=message.chat.id, reply_to_message_id=message.id)
        await asyncio.sleep(300)  # ৫ মিনিট
        try:
            await sent.delete()
        except:
            pass


app.run()
