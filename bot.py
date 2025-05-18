from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

app = Flask(__name__)

# তোমার Telegram Bot Token এখানে বসাও
BOT_TOKEN = "8124429702:AAGN2Wk9_R3F_tgArbgsJRj5M3u4HRjs6nE"

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# সিম্পল /start কমান্ড
def start(update, context):
    update.message.reply_text(
        "হ্যালো! আমি মুভি ডাউনলোড বট।\n"
        "তুমি /latest কমান্ড দিয়ে নতুন মুভির লিস্ট দেখতে পারবে।"
    )

# মুভির একটা সিম্পল লিস্ট (তুমি পরে ডাটাবেজ বা API থেকে নিয়ে দিবে)
MOVIES = [
    {"name": "Movie 1", "download_link": "https://example.com/movie1-download", "watch_link": "https://example.com/movie1-watch"},
    {"name": "Movie 2", "download_link": "https://example.com/movie2-download", "watch_link": "https://example.com/movie2-watch"},
    {"name": "Movie 3", "download_link": "https://example.com/movie3-download", "watch_link": "https://example.com/movie3-watch"},
]

def latest(update, context):
    keyboard = []
    for i, movie in enumerate(MOVIES):
        keyboard.append([InlineKeyboardButton(movie["name"], callback_data=f"movie_{i}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("নতুন মুভিগুলো দেখুন:", reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    query.answer()

    data = query.data
    if data.startswith("movie_"):
        index = int(data.split("_")[1])
        movie = MOVIES[index]

        text = f"🎬 {movie['name']}\n\n"
        text += f"[ডাউনলোড]({movie['download_link']}) | [ওয়াচ]({movie['watch_link']})"

        # Telegram markdown formatting এ লিংক পাঠাতে parse_mode=True দিতে হবে
        query.edit_message_text(text=text, parse_mode="Markdown", disable_web_page_preview=True)

# হ্যান্ডলার গুলো রেজিস্টার করো
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("latest", latest))
dispatcher.add_handler(CallbackQueryHandler(button))

# Flask route for Telegram webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
