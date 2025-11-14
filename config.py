import dotenv
from os import getenv


class TG:
	def __init__(self):
		dotenv.load_dotenv()
		self.token = getenv("TELEGRAM_TOKEN")
		self.chat_id = getenv("TELEGRAM_CHAT_ID")


class DB:
	def __init__(self):
		dotenv.load_dotenv()
		self.host = getenv("DB_HOST")
		self.port = getenv("DB_PORT")
		self.user = getenv("DB_USER")
		self.password = getenv("DB_PASSWORD")
		self.name = getenv("DB_NAME")


class RedisConf():
	""" Redis settings """
	def __init__(self) -> None:
		dotenv.load_dotenv()
		self.host = getenv('REDIS_HOST')
		self.port = int(getenv('REDIS_PORT', 6379))
		self.db = int(getenv('REDIS_DB', 0))
		self.channel = getenv('REDIS_CHANNEL')
