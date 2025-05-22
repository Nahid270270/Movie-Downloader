import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid

# Telegram Bot Token (বটের জন্য)
BOT_TOKEN = "your_bot_token_here"

# Telegram API ID & HASH (user session জন্য)
API_ID = 1234567
API_HASH = "your_api_hash_here"

# ইউজার সেশন স্ট্রিং (User session string, ইউজার অ্যাকাউন্টের)
USER_SESSION = "your_user_session_string_here"

# সার্চ করার চ্যানেল আইডি (ইনটিজার)
SOURCE_CHANNEL = -1002653036072

# মেসেজ অটো-ডিলিট সময় (সেকেন্ড)
AUTO_DELETE_TIME = 300  # ৫ মিনিট

# বট Client (Bot Token দিয়ে)
bot = Client("bot", bot_token=BOT_TOKEN)

# ইউজার Client (User Session দিয়ে)
user = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=USER_SESSION)


@bot.on_message(filters.private | filters.group & filters.text)
async def search_movie(bot_client: Client, message: Message):
    query = message.text.strip()
    if not query:
        await message.reply_text("অনুগ্রহ করে মুভির নাম লিখুন।")
        return

    try:
        # ইউজার সেশন থেকে সার্চ শুরু
        results = []
        async for msg in user.search_messages(SOURCE_CHANNEL, query=query, limit=5):
            results.append(msg)

        if not results:
            await message.reply_text("কোনো মুভি পাওয়া যায়নি আপনার অনুসন্ধানে।")
            return

        for msg in results:
            sent_msg = await message.reply_text(f"🔍 পাওয়া গেছে:\n\n{msg.text or 'No text content'}")
            await asyncio.sleep(AUTO_DELETE_TIME)
            await sent_msg.delete()

    except PeerIdInvalid:
        await message.reply_text("চ্যানেল আইডি সঠিক নয় অথবা ইউজার ওই চ্যানেলের মেম্বার নয়।")
    except Exception as e:
        await message.reply_text(f"ত্রুটি ঘটেছে: {e}")


async def main():
    # দুটো Client একসাথে স্টার্ট করবো
    await user.start()
    await bot.start()
    print("Bot & User session started")
    await bot.idle()
    await user.stop()
    await bot.stop()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
