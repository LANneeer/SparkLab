from aiogram import types, Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from bot.infrastructure.states.main import RegistrationState
from bot.infrastructure.keyboards.default.user import user_menu
from bot.infrastructure.keyboards.default.manager import manager_menu
from users.models import User

router = Router(name='menu')


@router.message(CommandStart(deep_link=True))
async def hello(message: types.Message, state: FSMContext, command: CommandObject):
    welcome_message = '<b>Привет! Добро пожаловать в бот проекта tezzhet.</b>\n' \
                      '<a href="https://t.me/almaty_transport_bot">tezzhet</a> - сервис бронирования удобных поездок для' \
                      ' студентов с акцентом на социальную справедливость! \U0001F697 \U0001F697 \n\n' \
                      '<b>Правила пользования:</b>\n' \
                      '1. Для начала бот попросит заполнить информацию о себе (пожалуйста вводите достоверную информацию для корректного подтверждения оплаты).\n' \
                      '2. Проверьте доступные варианты и выберите подходящий для вас.\n' \
                      '3. Произведите полную предоплату и ожидайте подтверждения от модератора. Пожалуйста, ' \
                      'имейте ввиду, что предоплата возвращается в случае отмены бронирования не менее чем за ' \
                      '24 часа до поездки. Место считается забронированным только после полной предоплаты.\n' \
                      '4. Следуйте инструкциям бота для завершения процесса бронирования.\n' \
                      '5. В случае возникновения вопросов или проблем обращайтесь к команде /help.\n\n' \
                      'Пожалуйста, обратите внимание, что наш бот находится на стадии разработки, поэтому возможны ' \
                      'некоторые ограничения и недоработки. Мы работаем над улучшением функционала и обновлениями, ' \
                      'чтобы сделать ваше путешествие еще более удобным и приятным.\n'
    await message.answer(text=welcome_message)
    if not User.objects.filter(telegram_id=message.from_user.id).exists():
        args = command.args
        if args:
            User.objects.create_user(username=message.from_user.username, telegram_id=message.from_user.id,
                                     is_staff=True, is_admin=True)
        else:
            User.objects.create_user(username=message.from_user.username, telegram_id=message.from_user.id)
        await message.answer(
            text='Для начала работы введи своё имя.'
        )
        await state.set_state(RegistrationState.first_name)
    else:
        if User.objects.get(telegram_id=message.from_user.id).is_admin:
            await message.answer(
                text='Теперь ты можешь воспользоваться меню команд /menu',
                reply_markup=manager_menu
            )
        else:
            await message.answer(
                text='Теперь ты можешь воспользоваться меню команд /menu',
                reply_markup=user_menu
            )


@router.message(RegistrationState.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    user = User.objects.get(telegram_id=message.from_user.id)
    user.first_name = message.text
    user.save()
    await message.answer(text='Теперь введи свою фамилию.')
    await state.set_state(RegistrationState.last_name)


@router.message(RegistrationState.last_name)
async def get_last_name(message: types.Message, state: FSMContext):
    user = User.objects.get(telegram_id=message.from_user.id)
    user.last_name = message.text
    user.save()
    if User.objects.get(telegram_id=message.from_user.id).is_admin:
        await message.answer(
            text='Теперь ты можешь воспользоваться меню команд /menu',
            reply_markup=manager_menu
        )
    else:
        await message.answer(
            text='Теперь ты можешь воспользоваться меню команд /menu',
            reply_markup=user_menu
        )
    await state.clear()
