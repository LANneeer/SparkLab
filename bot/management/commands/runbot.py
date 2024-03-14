from django.core.management.base import BaseCommand
import django

from bot.infrastructure.handlers import dp
from bot.apps import BotConfig
from bot.management.commands._private import on_startup, on_shutdown
import asyncio
import os


async def main() -> None:
    await on_startup(dp)
    await dp.start_polling(BotConfig.bot)
    await on_shutdown(dp)


class Command(BaseCommand):
    def handle(self, *args, **options):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackathon.hackathon.settings')
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        django.setup()
        asyncio.run(
            main()
        )
