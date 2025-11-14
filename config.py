import dotenv
from os import getenv


class TG:
    """Конфигурация для Telegram бота."""
    def __init__(self):
        dotenv.load_dotenv()
        self.token = getenv("TELEGRAM_TOKEN")
        self.chat_id = getenv("TELEGRAM_CHAT_ID")


class DB:
    """Конфигурация для подключения к базе данных MySQL."""
    def __init__(self):
        dotenv.load_dotenv()
        self.host = getenv("DB_HOST")
        self.port = getenv("DB_PORT")
        self.user = getenv("DB_USER")
        self.password = getenv("DB_PASSWORD")
        self.name = getenv("DB_NAME")


class RedisConf:
    """Конфигурация для подключения к Redis."""
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.host = getenv('REDIS_HOST')
        self.port = int(getenv('REDIS_PORT', 6379))
        self.db = int(getenv('REDIS_DB', 0))
        self.channel = getenv('REDIS_CHANNEL')


class Webhook:
    """Конфигурация для webhook URL."""
    def __init__(self):
        dotenv.load_dotenv()
        self.url = getenv("WEBHOOK_URL")