import os
import threading
from flask import Flask
import telebot
from groq import Groq

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL_ID = os.environ.get("MODEL_ID", "llama-3.1-8b-instant")

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        user_text = message.text
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Reply in the same language as user, default Bengali."},
                {"role": "user", "content": user_text}
            ]
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, f"Error: {e}")

def run_bot():
    bot.remove_webhook()
    bot.infinity_polling(none_stop=True, skip_pending=True)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
