from telebot import types


def start_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Да, хочу", "нет")
    return markup


def activity_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Низкая", "Средняя", "Высокая")
    return markup
    
def result_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🔁 Попробовать снова", "🔙 Назад")
    markup.add("Изменить рост", "Изменить вес")
    markup.add("Изменить цель")

    return markup