from aiogram import types, Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from bot.infrastructure.keyboards.default.manager import manager_menu
from bot.infrastructure.keyboards.default.user import user_menu
from bot.infrastructure.states.main import RegistrationState
from bot.infrastructure.texts.main import welcome_text
from users.models import User

router = Router(name='registration')


@router.message(CommandStart())
async def hello(message: types.Message, state: FSMContext, command: CommandObject):
    welcome_message = welcome_text
    await message.answer(text=welcome_message)
    if not User.objects.filter(telegram_id=message.from_user.id).exists():
        args = command.args
        if args:
            User.objects.create_user(username=message.from_user.username, telegram_id=message.from_user.id,
                                     is_staff=True, is_admin=True)
        else:
            User.objects.create_user(username=message.from_user.username, telegram_id=message.from_user.id)
        await message.answer(
            text='<b>Для начала работы введи ваше <i>имя</i></b>'
        )
        await state.set_state(RegistrationState.first_name)
    else:
        if User.objects.get(telegram_id=message.from_user.id).is_admin:
            await message.answer(
                text='Вы уже зарегистрированы❗',
                reply_markup=manager_menu
            )
        else:
            await message.answer(
                text='Вы уже зарегистрированы❗',
                reply_markup=user_menu
            )


@router.message(RegistrationState.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    user = User.objects.get(telegram_id=message.from_user.id)
    user.first_name = message.text
    user.save()
    await message.answer(text='<b>Введите вашу <i>фамилию</i></b>')
    await state.set_state(RegistrationState.last_name)


@router.message(RegistrationState.last_name)
async def get_last_name(message: types.Message, state: FSMContext):
    user = User.objects.get(telegram_id=message.from_user.id)
    user.last_name = message.text
    user.save()
    await message.answer(
        text='<b>Введи ваш номер <i>телефона</i></b>',
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text='Отправить номер телефона📱', request_contact=True)
                ]
            ],
            resize_keyboard=True
        )
    )
    await state.set_state(RegistrationState.phone)


@router.message(RegistrationState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    user = User.objects.get(telegram_id=message.from_user.id)
    user.payment_phone = message.text
    user.save()
    if user.is_admin:
        await message.answer(
            text='Вы успешно зарегистрировались как администратор!🎉',
            reply_markup=manager_menu
        )
    else:
        await message.answer(
            text='Вы успешно зарегистрировались как пользователь!🎉',
            reply_markup=user_menu
        )
    await state.clear()
