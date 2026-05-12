from fsm import get_step, set_step, update_field, reset, get_user
from logic import calculate_plan
from keyboards import activity_keyboard, result_keyboard
from telebot.types import ReplyKeyboardRemove
from telebot.apihelper import ApiTelegramException
import re
from logger_config import logger


# ---------------- SAFE SEND ----------------
def safe_send(bot, chat_id, text, reply_markup=None):
    try:
        logger.info(f"[SEND] {chat_id} -> {text}")
        bot.send_message(chat_id, text, reply_markup=reply_markup)

    except ApiTelegramException as e:
        logger.error(f"[TELEGRAM ERROR] {chat_id} -> {e}")

        if "403" in str(e):
            logger.warning(f"[BLOCKED USER] {chat_id}")
            reset(str(chat_id))

# ---------------- PARSE NUMBER ----------------
def parse_number(text: str):
    if not text:
        return None
    match = re.search(r"\d+(\.\d+)?", text)
    return float(match.group()) if match else None


# ---------------- HEIGHT ----------------
def handle_height(bot, message, user_id, text):
    logger.info("ENTER HEIGHT HANDLER")
    
    value = parse_number(text)
    if value is None:
    	   safe_send(bot, message.chat.id, "Введи число от 100 до 250")
    	   return
    if not (100 <= value <= 250):
    	   safe_send(bot, message.chat.id, "Рост должен быть от 100 до 250 см")
    	   return
    	
    update_field(user_id, "height", value)
    set_step(user_id, "weight")
    	
    safe_send(bot, message.chat.id, "Теперь вес:")


# ---------------- WEIGHT ----------------
def handle_weight(bot, message, user_id, text):
    logger.info("ENTER WEIGHT HANDLER")
    
    value = parse_number(text)

    if value is None:
        safe_send(bot, message.chat.id, "Введи число от 30 до 200")
        return

    if not (30 <= value <= 200):
        safe_send(bot, message.chat.id, "Вес должен быть от 30 до 200 кг")
        return

    update_field(user_id, "weight", value)
    set_step(user_id, "goal")

    safe_send(bot, message.chat.id, "Какой вес хочешь достичь?")


# ---------------- GOAL ----------------
def handle_goal(bot, message, user_id, text):
    logger.info("ENTER GOAL HANDLER")
    
    value = parse_number(text)

    if value is None:
        safe_send(bot, message.chat.id, "Введи число")
        return

    if not (30 <= value <= 200):
        safe_send(bot, message.chat.id, "Цель должна быть от 30 до 200 кг")
        return

    user = get_user(user_id)

    current_weight = user.get("weight")
    if current_weight is None:
        safe_send(bot, message.chat.id, "Сначала введи вес")
        set_step(user_id, "weight")
        return

    if abs(current_weight - value) > 50:
        safe_send(bot, message.chat.id, "Слишком большая разница. Введи реалистичную цель")
        return

    update_field(user_id, "goal", value)
    set_step(user_id, "activity")

    safe_send(
        bot,
        message.chat.id,
        "Выбери активность:",
        reply_markup=activity_keyboard()
    )


# ---------------- ACTIVITY ----------------
def handle_activity(bot, message, user_id, text):
    logger.info("ENTER ACTIVITY HANDLER")
    
    activity_map = {
        "Низкая": "low",
        "Средняя": "medium",
        "Высокая": "high"
    }

    if text not in activity_map:
        safe_send(bot, message.chat.id, "Выбери кнопку")
        return

    activity = activity_map[text]

    update_field(user_id, "activity", activity)
    set_step(user_id, "done")

    user = get_user(user_id)

    required = ["height", "weight", "goal", "activity"]
    if not all(k in user for k in required):
        safe_send(bot, message.chat.id, "Ошибка данных, начни заново /start")
        reset(user_id)
        return

    result = calculate_plan(
        user["height"],
        user["weight"],
        user["goal"],
        user["activity"]
    )

    safe_send(
        bot,
        message.chat.id,
        f"""
Цель: {result['target']}
Разница: {result['difference']} кг
Калории: {result['calories']} ккал

{result['recommendation']}
""",
        reply_markup=result_keyboard()
    )


# ---------------- DONE ----------------
def handle_done(bot, message, user_id, text):
	logger.info("ENTER DONE HANDLER")
	
	if text == "Изменить рост":
	      set_step(user_id, "height")
	      safe_send(bot, message.chat.id, "Введи рост")
	      return
	
	if text == "Изменить вес":
	       set_step(user_id, "weight")
	       safe_send(bot, message.chat.id, "Введи вес")
	       return
	       
	if text == "Изменить цель":
	       set_step(user_id, "goal")
	       safe_send(bot, message.chat.id, "Введи цель")
	       return
	
	safe_send(bot, message.chat.id, "Выбери кнопку")


# ---------------- REGISTER ----------------
def register_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = str(message.chat.id)

        reset(user_id)

        set_step(user_id, "height")

        safe_send(bot, message.chat.id, "Введи рост:")
    
    
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
    	try:
    		user_id = str(message.chat.id)
    		text = (message.text or "").strip()
    		user = get_user(user_id)
    		
    		step = get_step(user_id)
    		
    		logger.info(f"USER: {user_id}")
    		logger.info(f"STEP: {step}")
    		logger.info(f"TEXT: {repr(text)}")
    		
    		if not user:
    		  safe_send(bot, message.chat.id, "Нажми /start")
    		  return
    		
    		if step not in ["height", "weight", "goal", "activity", "done"]:
    		      logger.error(f"UNKNOWN STEP: {step}")
    		      safe_send(bot, message.chat.id, "Ошибка состояния, /start")
    		      return

    		if step == "height":
    			handle_height(bot, message, user_id, text)
    		elif step == "weight":
    			handle_weight(bot, message, user_id, text)
    		elif step == "goal":
    			handle_goal(bot, message, user_id, text)
    		elif step == "activity":
    			handle_activity(bot, message, user_id, text)
    		elif step == "done":
    			handle_done(bot, message, user_id, text)
    		else:
    			print("UNKNOWN STEP:", repr(step))
    			safe_send(bot, message.chat.id, "Ошибка состояния, /start")
    	
    	except Exception:
    		logger.exception("ROUTER CRASH")