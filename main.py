import os, asyncio, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
BOT_TOKEN=os.environ.get("BOT_TOKEN")
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
app=Flask(__name__)
@app.route('/')
def home(): return "AUREX ONE Live!"
client=Groq(api_key=GROQ_API_KEY)
async def start(update, context): await update.message.reply_text("হ্যালো ভাই! আমি AUREX ONE")
async def chat(update, context):
    try:
        c=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=[{"role":"user","content":update.message.text}])
        await update.message.reply_text(c.choices[0].message.content)
    except Exception as e: await update.message.reply_text(f"Error: {e}")
def run_bot():
    async def main_bot():
        application=Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start",start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,chat))
        await application.initialize(); await application.start(); await application.updater.start_polling(); await asyncio.Event().wait()
    loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(main_bot())
def run_flask(): app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
if __name__=="__main__":
    threading.Thread(target=run_flask,daemon=True).start()
    run_bot()
