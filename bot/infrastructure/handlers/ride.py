from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from django.utils import timezone

from bot.infrastructure.keyboards.default.user import user_menu
from bot.infrastructure.states.main import ReportState, CommentState, RideState
from rides.models import Ride, RideRequest
from users.models import Report, User, Comment, ModerateSchedule

router = Router(name='ride')


@router.message(F.text == "Забронировать поездку")
async def send_ride(message: types.Message, state: FSMContext):
    rides = Ride.objects.filter(departure__gte=timezone.now(),
                                departure__lte=timezone.now() + timezone.timedelta(days=7))
    rides = rides.order_by('departure')
    rides = rides.values('departure').distinct()
    rides = [ride['departure'] for ride in rides]
    rides = [ride.strftime('%d.%m.%Y') for ride in rides]
    await state.set_state(RideState.ride)
    if not rides:
        await message.answer(
            text='К сожалению, ближайших поездок нет.',
            reply_markup=user_menu
        )
        await state.clear()
    else:
        await message.answer(
            text='Выберите дату поездки:',
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [
                        types.KeyboardButton(text=ride)
                    ] for ride in rides
                ],
                resize_keyboard=True
            )
        )


@router.message(RideState.ride)
async def get_ride(message: types.Message, state: FSMContext):
    departure = timezone.datetime.strptime(message.text, '%d.%m.%Y')
    rides = Ride.objects.filter(departure__gte=departure, departure__lte=departure + timezone.timedelta(days=1))
    rides = rides.order_by('departure')
    rides = rides.values('departure', 'ride_title')
    rides = [f"{ride['ride_title']} - {ride['departure'].strftime('%H:%M')}" for ride in rides]
    await state.set_state(RideState.payment)
    await message.answer(
        text='Выберите поездку:',
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text=ride)
                ] for ride in rides
            ],
            resize_keyboard=True
        )
    )


@router.message(RideState.payment)
async def confirm_ride(message: types.Message, state: FSMContext):
    ride = Ride.objects.get(ride_title=message.text.split(' - ')[0])
    manager = ModerateSchedule.objects.filter(date=message.date).first().user
    RideRequest.objects.create(
        user=User.objects.get(telegram_id=message.from_user.id),
        ride=ride,
        status='pending',
    )
    await state.set_state(RideState.confirm)
    await message.answer(
        text=f'Оплатите 450тг на этот номер через каспи: '
             f'{manager.payment_phone} - {manager.first_name} {manager.last_name[:1]}.\n',
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text='Подтвердить оплату')
                ],
                [
                    types.KeyboardButton(text='Назад')
                ],
            ],
            resize_keyboard=True
        )
    )


@router.message(RideState.confirm)
async def confirm_payment(message: types.Message, state: FSMContext):
    if message.text == 'Подтвердить оплату':
        user = User.objects.get(telegram_id=message.from_user.id)
        manager = ModerateSchedule.objects.filter(date=message.date).first().user
        ride = RideRequest.objects.filter(user=user, status='pending').first()
        await message.bot.send_message(
            chat_id=manager.telegram_id,
            text=f'{user.first_name} {user.last_name} оплатил поездку: \n'
                 f'{ride.ride_title} - {ride.departure.strftime("%a %d - %H:%M")} '
                 f'- {ride.arrival.strftime("%d.%m.%Y")}\n'
                 f'Подтвердите или отклоните его заявку.',
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm_{ride.id}')
                    ],
                    [
                        types.InlineKeyboardButton(text='Отклонить', callback_data=f'decline_{ride.id}')
                    ]
                ]
            )
        )
        await message.answer(
            text=f'Ожидайте подтверждения от менеджера.\n',
            reply_markup=user_menu
        )
        await state.clear()
    else:
        await message.answer(
            text='Поездка отменена.',
            reply_markup=user_menu
        )
        await state.clear()


@router.message(F.text == "Мои поездки")
async def my_rides(message: types.Message):
    user = User.objects.get(telegram_id=message.from_user.id)
    text = "\n".join([f"{ride.ride_title} - {ride.departure.strftime('%a %d - %H:%M')}" for ride in user.rides.all()])
    await message.answer(
        text=text,
        reply_markup=user_menu
    )


@router.message(F.text == "Получить помощь")
async def get_help(message: types.Message):
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


@router.message(F.text == "Оставить отзыв")
async def send_comment(message: types.Message, state: FSMContext):
    await state.set_state(CommentState.comment)
    await message.answer(
        text='Напишите ваш отзыв:',
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(CommentState.comment)
async def write_comment(message: types.Message, state: FSMContext):
    user = User.objects.get(telegram_id=message.from_user.id)
    Comment.objects.create(user=user, comment=message.text)
    await message.answer(
        text='Ваш отзыв отправлен. Спасибо за обратную связь!',
        reply_markup=user_menu
    )
    await state.clear()
