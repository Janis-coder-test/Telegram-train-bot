from telebot import types
from storage import load_users, save_users
from logic import calculate_plan
from keyboards import start_keyboard, activity_keyboard
from telebot.types import ReplyKeyboardRemove
from telebot.apihelper import ApiTelegramException

def safe_send(bot, chat_id, text, reply_markup=None):
    try:
        bot.send_message(chat_id, text, reply_markup=reply_markup)
    except ApiTelegramException as e:
        if e.error_code == 403:
            print(f"[BLOCKED USER] {chat_id}")
        else:
            print(f"[TELEGRAM ERROR] {e}")


def register_handlers(bot):

    # --- /start ---
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = start_keyboard()
        
        safe_send(bot,
            message.chat.id,
            "Привет! Я помогу рассчитать план для похудения или набора веса.\nХочешь попробовать?",
            reply_markup=markup
        )

    # --- обработка всех сообщений ---
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        user_id = str(message.chat.id)
        users = load_users()

        if user_id not in users:
            users[user_id] = {}

        text = message.text

        # --- старт ввода ---
        if text == "Да, хочу":
            users[user_id]["step"] = "height"
            save_users(users)

            safe_send(bot, message.chat.id, "Введи свой рост (см):", reply_markup=ReplyKeyboardRemove())
            return

        step = users[user_id].get("step")

        # --- ввод роста ---
        if step == "height":
            if not text.isdigit():
                safe_send(bot, message.chat.id, "Введи число.")
                return

            users[user_id]["height"] = int(text)
            users[user_id]["step"] = "weight"
            save_users(users)

            safe_send(bot, message.chat.id, "Теперь введи вес (кг):")
            return

        # --- ввод веса ---
        if step == "weight":
            if not text.isdigit():
                safe_send(bot, message.chat.id, "Введи число.")
                return

            users[user_id]["weight"] = int(text)
            users[user_id]["step"] = "goal"
            save_users(users)

            safe_send(bot, message.chat.id, "Какой вес хочешь достичь?")
            return

        # --- ввод цели ---
        if step == "goal":
            if not text.isdigit():
                safe_send(bot, message.chat.id, "Введи число.")
                return

            users[user_id]["goal"] = int(text)
            users[user_id]["step"] = "activity"
            save_users(users)

            markup = activity_keyboard()
            
            safe_send(bot, 
                message.chat.id,
                "Выбери уровень активности:",
                reply_markup=markup
            )
            return

        # --- активность ---
        if step == "activity":
            activity_map = {
                "Низкая": "low",
                "Средняя": "medium",
                "Высокая": "high"
            }

            if text not in activity_map:
                safe_send(bot, message.chat.id, "Выбери кнопку.")
                return

            users[user_id]["activity"] = activity_map[text]

            # --- расчёт ---
            result = calculate_plan(
                users[user_id]["height"],
                users[user_id]["weight"],
                users[user_id]["goal"],
                users[user_id]["activity"]
            )

            users[user_id]["step"] = "activity"
            save_users(users)

            safe_send(bot, 
                message.chat.id,
                f"""
Цель: {result['target']}
Разница: {result['difference']} кг
Калории: {result['calories']} ккал

{result['recommendation']}
"""
            )
            return

        # --- fallback ---
        safe_send(bot, message.chat.id, "Нажми /start чтобы начать")