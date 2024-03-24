from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.infrastructure.keyboards.default.manager import manager_menu
from bot.infrastructure.keyboards.default.user import user_menu
from bot.infrastructure.states.main import MenuState
from users.models import User

router = Router(name='menu')


@router.message(Command("menu"))
async def menu(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.menu)
    if User.objects.get(telegram_id=message.from_user.id).is_admin:
        await message.answer(
            text='<b>Меню</b>',
            reply_markup=manager_menu
        )
    else:
        await message.answer(
            text='<b>Меню</b>',
            reply_markup=user_menu
        )
