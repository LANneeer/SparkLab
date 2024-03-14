from aiogram import Router, types
from aiogram.filters import Command

router = Router(name='help')


@router.message(Command("help"))
async def menu(message: types.Message):
    await message.answer(
        text='<b>Помощь</b>\n'
             'Для начала работы введите команду /start\n'
             'Для вызова меню введите команду /menu'
    )
