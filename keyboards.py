from telebot import types


def start_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Да, хочу")
    return markup


def activity_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Низкая", "Средняя", "Высокая")
    return markup