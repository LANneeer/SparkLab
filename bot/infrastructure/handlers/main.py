from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from bot.apps import BotConfig
from bot.infrastructure.states.main import Main
from users.models import User

bot = BotConfig.bot
dp = BotConfig.dp


@dp.message(CommandStart())
async def hello(message: types.Message):
    if not User.objects.filter(telegram_id=message.from_user.id).exists():
        User.objects.create_user(username=message.from_user.username, telegram_id=message.from_user.id)
    await message.answer(text=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                              'Жми на кнопку ‘Меню’ ниже, чтобы узнать, что я умею.'
                         )


@dp.message(Command("menu"))
async def menu(message: types.Message, state: FSMContext):
    await state.set_state(Main.menu)
    await message.answer(
        text='<b>Меню</b>',
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text='Получить помощь')
                ],
                [
                    types.KeyboardButton(text='Узнать о загруженности общественного транспорта')
                ],
                [
                    types.KeyboardButton(text='о загруженности общественного транспорта')
                ],
                [
                    types.KeyboardButton(text='Оставить отзыв/предложения')
                ]
            ],
            resize_keyboard=True
        )
    )
