import os
import threading
from flask import Flask
import telebot
import html

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN পাওয়া যায়নি! Render Environment এ বসান।")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "AUREX ONE is Live!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "AUREX ONE Active! এখন যা লিখবেন Copy অপশন সহ পাবেন।")

@bot.message_handler(content_types=['text'])
def copy_handler(message):
    if message.text.startswith('/'):
        return
    safe_text = html.escape(message.text)
    bot.send_message(message.chat.id, f"<code>{safe_text}</code>", parse_mode="HTML")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    bot.delete_webhook()
    print("Bot polling started...")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
