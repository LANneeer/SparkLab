from django.core.management.base import BaseCommand
from bot.apps import BotConfig
from users.models import User
import asyncio
from asgiref.sync import sync_to_async


class Command(BaseCommand):
    async def send_messages(self, bot, text):
        users = await sync_to_async(list)(User.objects.filter(is_staff=False))
        for user in users:
            try:
                await bot.send_message(chat_id=user.telegram_id, text=text)
            except Exception as e:
                print(f"Failed to send message to {user.telegram_id}: {e}")

    def handle(self, *args, **options):
        bot = BotConfig.bot
        text = "<b>Привет! Благодарим за доверие к нашему сервису.</b>\n" \
                "16 апреля у нас будет специальное предложение: <u><b>поездка всего за 300 тенге!</b></u>\n\n" \
                "Выбери удобное время отправления:\n" \
                "1. 09:10 с Dorm KBTU\n" \
                "2. 10:10 с Dorm KBTU\n" \
                "3. 11:10 с Dorm KBTU\n\n" \
                "Переходи в меню и бронируй поездку на завтра!"
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_messages(bot, text))
        loop.close()


