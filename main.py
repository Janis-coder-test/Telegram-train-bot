import telebot
from handlers import register_handlers
from config import BOT_TOKEN
import logging

bot = telebot.TeleBot(BOT_TOKEN)

register_handlers(bot)

print("Бот запущен...")

try:
	bot.polling(none_stop=True, interval=0, timeout=20)
except Exception:
    logging.exception("BOT CRASH")