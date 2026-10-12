import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# Render এর জন্য Web Server
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "AUREX ONE Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host='0.0.0.0', port=port)

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")
client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আসসালামু আলাইকুম ভাই! আমি AUREX ONE Live! বলেন কিভাবে হেল্প করতে পারি?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_msg = update.message.text
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": user_msg}],
            temperature=0.7,
            max_tokens=1024
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(f"Error: {e}")

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
