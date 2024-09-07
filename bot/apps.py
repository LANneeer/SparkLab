from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from django.apps import AppConfig
from aiogram import Bot, Dispatcher, types

from SparkLab.env import env


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"
    bot_token = env("BOT_TOKEN")
    webhook_host = env("WEBHOOK_HOST")
    webhook_path = env("WEBHOOK_PATH")
    webhook_url = f"{webhook_host}{webhook_path}"
    webapp_host = "localhost"
    webapp_port = 3001
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
