from aiogram import types
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.utils.payload import decode_payload

from bot.apps import BotConfig
from bot.infrastructure.states.main import RegistrationState, MenuState
from users.models import User

bot = BotConfig.bot
dp = BotConfig.dp


@dp.message(CommandStart(deep_link=True))
async def hello(message: types.Message, state: FSMContext, command: CommandObject):
    if not User.objects.filter(telegram_id=message.from_user.id).exists():
        args = command.args
        if args:
            User.objects.create_user(username=message.from_user.username, telegram_id=message.from_user.id,
                                     is_staff=True, is_admin=True)
        else:
            User.objects.create_user(username=message.from_user.username, telegram_id=message.from_user.id)
        await message.answer(text=f'Привет, {message.from_user.username}! Я бот, который поможет тебе забронировать место '
                                  f'в транспорте. Для начала работы введи своё имя.'
                             )
        await state.set_state(RegistrationState.first_name)
    else:
        await message.answer(text=f'Привет, {message.from_user.username}! Я рад видеть тебя снова. '
                                  f'Ты можешь воспользоваться меню команд /menu'
                             )


@dp.message(RegistrationState.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    user = User.objects.get(telegram_id=message.from_user.id)
    user.first_name = message.text
    user.save()
    await message.answer(text='Теперь введи свою фамилию.')
    await state.set_state(RegistrationState.last_name)


@dp.message(RegistrationState.last_name)
async def get_last_name(message: types.Message, state: FSMContext):
    user = User.objects.get(telegram_id=message.from_user.id)
    user.last_name = message.text
    user.save()
    await message.answer(text='Теперь ты можешь воспользоваться меню команд /menu')
    await state.clear()


@dp.message(Command("menu"))
async def menu(message: types.Message, state: FSMContext):
    await state.set_state(MenuState.menu)
    if User.objects.get(telegram_id=message.from_user.id).is_admin:
        await message.answer(
            text='<b>Меню</b>',
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        types.KeyboardButton(text='Просмотреть пользователей')
                    ],
                    [
                        types.KeyboardButton(text='Просмотреть отзывы/предложения')
                    ],
                    [
                        types.KeyboardButton(text='Просмотреть поездки')
                    ]
                ],
                resize_keyboard=True
            )
        )
    else:
        await message.answer(
            text='<b>Меню</b>',
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        types.KeyboardButton(text='Забронировать поездку')
                    ],
                    [
                        types.KeyboardButton(text='Мои поездки')
                    ],
                    [
                        types.KeyboardButton(text='Получить помощь')
                    ],
                    [
                        types.KeyboardButton(text='Оставить отзыв/предложения')
                    ]
                ],
                resize_keyboard=True
            )
        )
