import asyncio

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand

from bot.apps import BotConfig
from users.models import User


class Command(BaseCommand):
    async def send_messages(self, bot, text):
        users = await sync_to_async(list)(User.objects.filter(is_staff=False))
        for user in users:
            try:
                await bot.send_message(chat_id=user.telegram_id, text=text, disable_web_page_preview=True, parse_mode='HTML')
            except Exception as e:
                print(f"Failed to send message to {user.telegram_id}: {e}")

    def handle(self, *args, **options):
        bot = BotConfig.bot
        text = "<b>Привет, на связи UniShuttle!</b>\n" \
               "<b>Спасибо за доверие к нашему проекту.</b>\n" \
               "Мы успешно завершили тестовый период, организовав поездки для 162 пассажиров🤯🥳\n" \
               "Мы теперь сотрудничаем напрямую с водителями, без участия спонсора. <u>И в связи с этим вынуждены сообщить следующее:</u>\n" \
               "На основе результатов этих поездок мы пришли к выводу, что для обеспечения стабильной работы нашего проекта <b>необходимо повысить цену до 450 тенге</b>🚌\n" \
               "💓Нам очень важно ваше мнение, пожалуйста, пройдите очень короткий опрос по ссылке:\n" \
               "<i><a href='https://forms.gle/QXkh1NwBLufPEZxe7'>Ссылка</a></i>"
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_messages(bot, text))
        loop.close()
