import os
import telebot
import threading
import time
from flask import Flask
import google.generativeai as genai

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        user_text = message.text
        response = model.generate_content(user_text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "একটু সমস্যা হচ্ছে ভাই, আবার চেষ্টা করেন।")

def run_bot():
    while True:
        try:
            print("Bot polling started...")
            bot.infinity_polling(none_stop=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Polling crashed: {e}, restarting...")
            time.sleep(15)

app = Flask(__name__)
@app.route('/')
def home():
    return "AUREX-ONE Bot is Live!"

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
