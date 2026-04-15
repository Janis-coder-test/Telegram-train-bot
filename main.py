import telebot
from handlers import register_handlers
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

register_handlers(bot)

print("Бот запущен...")

bot.polling(none_stop=True)