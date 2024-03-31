from aiogram import Router, types
from aiogram.filters import Command

from users.models import ModerateSchedule

router = Router(name='help')


@router.message(Command("help"))
async def menu(message: types.Message):
    today_schedule = ModerateSchedule.objects.filter(date=message.date).first()
    if not today_schedule:
        await message.answer(
            text=f'<b>Помощь</b>\n'
                 f'Для получения помощи обратитесь к администратору.'
        )
    else:
        await message.answer(
            text=f'<b>Помощь</b>\n'
                 f'Для получения помощи обратитесь к администратору.'
                 f't.me/{today_schedule.user.username}'
        )
