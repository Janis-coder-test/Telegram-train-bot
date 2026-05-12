import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("bot.log", mode='w', encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)