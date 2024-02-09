from aiogram import types
from aiogram.fsm.context import FSMContext
from django.contrib.auth.models import User
from django.db.models import Q
from bot.apps import BotConfig
from aiogram.filters import Command, CommandStart
from asgiref.sync import sync_to_async

bot = BotConfig.bot
dp = BotConfig.dp


@dp.message(CommandStart())
async def hello(message: types.Message):
    await message.answer(text=f'<b>Привет, {message.from_user.first_name}!</b>'
                              'Жми на кнопку ‘Меню’ ниже, чтобы узнать, что я умею.'
                         )


@dp.message(Command("menu"))
async def menu(message: types.Message):
    await message.answer(text='<b>Меню</b>',
                         reply_markup=types.ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     types.KeyboardButton(text='Задать вопрос')
                                 ],
                                 [
                                     types.KeyboardButton(text='Посмотреть вопросы')
                                 ]
                             ],
                             resize_keyboard=True
                         )
                         )
