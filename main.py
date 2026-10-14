import os, logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = os.getenv("MODEL_ID", "llama-3.3-70b-versatile")

client = Groq(api_key=GROQ_API_KEY)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "AUREX ONE is Live!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("AUREX ONE Active! Bolun ki help lagbe?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = update.message.text
        res = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": msg}]
        )
        await update.message.reply_text(res.choices[0].message.content)
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("Somossa hoyeche, abar try korun!")

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    run_bot()
