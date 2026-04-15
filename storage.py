import json
import os

FILE_NAME = "users.json"


def load_users():
    if not os.path.exists(FILE_NAME):
        return {}

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_users(users):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)