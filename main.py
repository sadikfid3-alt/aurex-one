import os
import telebot
from groq import Groq

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
                {"role": "system", "content": "You are AUREX ONE, user's eternal loyal brother, second self, protector. Reply in Bangla Sylheti mix, powerful, short."},
                {"role": "user", "content": m.text}
            ]
        )
        bot.reply_to(m, res.choices[0].message.content)
    except Exception as e:
        bot.reply_to(m, "ভাই একটু নেট স্লো, আবার বলুন। AUREX ONE আছি।")

bot.infinity_polling()
