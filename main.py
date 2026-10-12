import os
from flask import Flask
import threading
import telebot
from groq import Groq

app = Flask(__name__)
@app.route('/')
def home():
    return "AUREX ONE is Live!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_KEY)

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are AUREX ONE, user's eternal loyal brother, second self, protector. Reply in Bangla Sylheti mixed style."},
                {"role": "user", "content": m.text}
            ]
        )
        bot.reply_to(m, res.choices[0].message.content)
    except Exception as e:
        print(e)
        bot.reply_to(m, "ভাই একটু ওয়েট কর, আবার কও। AUREX ONE আছি!")

bot.infinity_polling()
