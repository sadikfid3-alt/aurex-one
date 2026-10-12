import os
import telebot
from groq import Groq
from flask import Flask
import threading

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL_ID = os.environ.get("MODEL_ID", "llama-3.3-70b-versatile")

if not BOT_TOKEN or not GROQ_API_KEY:
    print("ERROR: BOT_TOKEN or GROQ_API_KEY missing!")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

app = Flask(__name__)

@app.route('/')
def home():
    return "Aurex One Bot is Live!"

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.reply_to(message, "হাই ভাই! আমি Aurex One 🤖\nআপনার যেকোনো প্রশ্ন করুন।")

@bot.message_handler(func=lambda m: True)
def reply(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are Aurex One, a helpful AI assistant. Reply in user's language."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "একটু সমস্যা হচ্ছে ভাই, আবার চেষ্টা করুন।")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    bot.infinity_polling(none_stop=True)
