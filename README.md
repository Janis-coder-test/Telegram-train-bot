# Telegram Fitness Bot

Телеграм-бот для расчёта калорий и целей по весу.

## Возможности

- Расчёт калорий
- FSM состояния
- Валидация ввода
- Выбор активности
- Изменение параметров
- Логирование ошибок

## Стек

- Python
- pyTelegramBotAPI
- JSON storage

## Запуск

### 1. Установить зависимости

```bash
pip install -r requirements.txt
```

### 2. Создать .env

```env
BOT_TOKEN=your_token
```

### 3. Запустить бота

```bash
python main.py
```

## Структура проекта

```text
main.py         # запуск бота
handlers.py     # обработка сообщений
fsm.py          # состояния
logic.py        # расчёты
storage.py      # работа с JSON
keyboards.py    # клавиатуры
config.py       # загрузка токена
```
