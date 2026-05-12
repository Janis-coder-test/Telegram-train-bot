from storage import load_users, save_users

# загружаем один раз при старте
USERS_CACHE = load_users()


# ---------------- CORE ----------------
def get_user(user_id):
    return USERS_CACHE.get(user_id)


def set_user(user_id, data):
    USERS_CACHE[user_id] = data


def set_step(user_id, step):
    if user_id not in USERS_CACHE:
        USERS_CACHE[user_id] = {}

    USERS_CACHE[user_id]["step"] = step


def get_step(user_id):
    return USERS_CACHE.get(user_id, {}).get("step")


def update_field(user_id, key, value):
    if user_id not in USERS_CACHE:
        USERS_CACHE[user_id] = {}

    USERS_CACHE[user_id][key] = value


# ---------------- RESET ----------------
def reset(user_id):
    USERS_CACHE[user_id] = {
        "step": "height"
    }


# ---------------- SAVE CONTROL ----------------
def save_state():
    save_users(USERS_CACHE)