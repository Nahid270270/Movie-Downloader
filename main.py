import asyncio
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message

# তোমার Telegram API credentials (https://my.telegram.org)
API_ID = 1234567  # তোমার API ID
API_HASH = "your_api_hash_here"  # তোমার API HASH

# ইউজার সেশন স্ট্রিং (Pyrogram user session string)
SESSION_STRING = "your_user_session_string_here"

# সার্চ করার জন্য চ্যানেল আইডি (ইনটিজার ফরম্যাটে, -100 দিয়ে শুরু করতে হবে)
SOURCE_CHANNEL = -1002653036072  # তোমার প্রাইভেট চ্যানেল আইডি

# Auto delete time in seconds
AUTO_DELETE_TIME = 300  # ৫ মিনিট

app = Client(session_name=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.private | filters.group & filters.text)
async def search_movie(client: Client, message: Message):
    query = message.text.strip()
    if not query:
        return await message.reply_text("অনুগ্রহ করে মুভির নাম লিখুন।")

    try:
        results = []
        async for msg in client.search_messages(SOURCE_CHANNEL, query=query, limit=5):
            # মুভি নাম ও লিঙ্ক টা নিতে পারো যদি মেসেজে থাকে
            results.append(msg)

        if not results:
            await message.reply_text("কোনো মুভি পাওয়া যায়নি আপনার অনুসন্ধানে।")
            return

        for msg in results:
            sent_msg = await message.reply_text(f"🔍 পাওয়া গেছে:\n\n{msg.text or 'No text content'}")
            # ৫ মিনিট পর মেসেজ ডিলিট করো
            await asyncio.sleep(AUTO_DELETE_TIME)
            await sent_msg.delete()

    except PeerIdInvalid:
        await message.reply_text("চ্যানেল আইডি সঠিক নয় বা বট/ইউজার সেই চ্যানেলটি দেখার অনুমতি পায়নি।")
    except Exception as e:
        await message.reply_text(f"ত্রুটি ঘটেছে: {e}")


if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
