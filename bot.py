from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "8124429702:AAGN2Wk9_R3F_tgArbgsJRj5M3u4HRjs6nE"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# একটা সিম্পল মুভি ডাটাবেস (তুমি চাইলে এক্সটেনশন দিবে)
MOVIE_DB = {
    "inception": {
        "watch": "https://example.com/inception/watch",
        "download": "https://example.com/inception/download"
    },
    "interstellar": {
        "watch": "https://example.com/interstellar/watch",
        "download": "https://example.com/interstellar/download"
    },
    "avengers": {
        "watch": "https://example.com/avengers/watch",
        "download": "https://example.com/avengers/download"
    }
}

def send_message(chat_id, text, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = reply_markup
    requests.post(f"{API_URL}/sendMessage", json=data)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()

    if "message" in update:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").lower().strip()

        # মুভির নাম যদি ডাটাবেসে থাকে
        if text in MOVIE_DB:
            movie = MOVIE_DB[text]
            buttons = {
                "inline_keyboard": [
                    [
                        {"text": "Watch", "url": movie["watch"]},
                        {"text": "Download", "url": movie["download"]}
                    ]
                ]
            }
            send_message(chat_id, f"<b>{text.title()}</b> মুভির লিংক নিচে:", reply_markup=buttons)
        else:
            send_message(chat_id, "দুঃখিত, আমাদের ডাটাবেসে এই মুভির তথ্য নেই। অনুগ্রহ করে অন্য মুভির নাম চেষ্টা করুন।")

    return "ok"

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
