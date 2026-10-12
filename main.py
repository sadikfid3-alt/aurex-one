import os
import threading
from flask import Flask
import telebot
from groq import Groq

# Render থেকে Token নিবে
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "Aurex One Bot is Live! ✅"

# বট সেটআপ
if not BOT_TOKEN:
    print("BOT_TOKEN missing!")
else:
    bot = telebot.TeleBot(BOT_TOKEN)
    groq_client = None
    if GROQ_API_KEY:
        groq_client = Groq(api_key=GROQ_API_KEY)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, "হ্যালো ভাই! আমি Aurex One ✅\nআপনার AI এজেন্ট এখন Live!\nআপনি যা বলবেন আমি তাই করবো।")

    @bot.message_handler(func=lambda m: True)
    def handle_all(message):
        user_text = message.text
        try:
            if groq_client:
                # Groq AI দিয়ে রিপ্লাই
                chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are Aurex One, a helpful AI assistant for Sadik. Reply in Bengali (Bangla) mix with English if needed. Be friendly."},
                        {"role": "user", "content": user_text}
                    ],
                    model="llama3-8b-8192",
                )
                reply = chat_completion.choices[0].message.content
                bot.reply_to(message, reply)
            else:
                bot.reply_to(message, f"আপনি বললেন: {user_text}\n\n(Groq API Key বসালে আমি AI এর মতো রিপ্লাই দিবো)")
        except Exception as e:
            print(f"Error: {e}")
            bot.reply_to(message, f"আপনি বললেন: {user_text}")

    def run_flask():
        port = int(os.environ.get("PORT", 10000))
        app.run(host='0.0.0.0', port=port)

    def run_bot():
        print("Bot Polling Started...")
        bot.infinity_polling()

    if __name__ == "__main__":
        threading.Thread(target=run_flask, daemon=True).start()
        run_bot()
