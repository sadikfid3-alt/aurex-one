import os
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "AUREX ONE - Boss Agent is Live!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "🔥 AUREX ONE Active Boss!\n\n"
        "আমি আপনার পার্সোনাল ম্যানেজার। কমান্ড দিন:\n"
        "/video - ভিডিও আইডিয়া / স্ক্রিপ্ট\n"
        "/customer - কাস্টমার রিপ্লাই\n"
        "/income - আজকের ইনকাম প্ল্যান\n\n"
        "আর যা লিখবেন, আমি ম্যানেজার হিসেবে হেল্প করব।"
    )

@bot.message_handler(commands=['video'])
def video_cmd(message):
    bot.reply_to(message,
        "🎬 VIDEO BOSS MODE:\n\n"
        "আপনার ডেনিমের জন্য আজকের ভিডিও:\n"
        "Hook: 'এই ৩টা ভুলে আপনার শার্ট নষ্ট হচ্ছে!'\n"
        "Scene 1: ফ্যাক্টরির কাপড়\n"
        "Scene 2: আপনার প্রোডাক্ট\n"
        "CTA: 'Inbox করুন'\n\n"
        "আপনি কি চান আমি পুরো স্ক্রিপ্ট লিখে দিই?"
    )

@bot.message_handler(commands=['customer'])
def customer_cmd(message):
    bot.reply_to(message,
        "💬 CUSTOMER BOSS MODE:\n\n"
        "কাস্টমারকে এই মেসেজ দিন:\n"
        "'ভাইয়া, আপনার সাইজটা বলেন, আমি ১০ মিনিটে ছবি সহ ডেলিভারি ডিটেইলস দিচ্ছি। ফ্রি রিটার্ন আছে।'\n\n"
        "কাস্টমারের মেসেজটা Forward করুন, আমি রিপ্লাই বানিয়ে দেব।"
    )

@bot.message_handler(commands=['income'])
def income_cmd(message):
    bot.reply_to(message,
        "💰 INCOME BOSS PLAN - আজকের জন্য:\n\n"
        "১. ২টা ভিডিও পোস্ট (১১টা ও ৮টা)\n"
        "২. ১০ জন পুরান কাস্টমারকে Knock দিন\n"
        "৩. একটা অফার বানান: '২টা নিলে ডেলিভারি ফ্রি'\n\n"
        "এই ৩টা করলে আজকেই সেল আসবে Boss। শুরু করব?"
    )

@bot.message_handler(content_types=['text'])
def boss_handler(message):
    text = message.text.lower()
    if "ভিডিও" in text or "video" in text:
        bot.reply_to(message, "ভিডিও বানাবো Boss? /video লিখুন, আমি স্ক্রিপ্ট রেডি করে দিচ্ছি।")
    elif "কাস্টমার" in text or "customer" in text:
        bot.reply_to(message, "কাস্টমার সামলাবো? /customer লিখুন বা কাস্টমারের মেসেজ Forward করুন।")
    else:
        bot.reply_to(message, f"বুঝেছি Boss: '{message.text}'\n\nএটা নিয়ে কি করতে হবে? ভিডিও বানাবো, নাকি কাস্টমারকে পাঠাবো? কমান্ড দিন: /video /customer /income")

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def run_bot():
    bot.delete_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
