from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def menu(message: types.Message):
    await message.answer(
        text='<b>Степени загруженности:</b>\n'
             '/level1 - Минимум людей, много мест\n'
             '/level2 - Небольшая загруженность, есть свободные места\n'
             '/level3 - Много людей, ограниченные места, дискомфорт'
    )
