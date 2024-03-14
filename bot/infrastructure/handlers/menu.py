from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from django.utils import timezone

from bot.infrastructure.states.main import ReportState, CommentState, RideState
from users.models import Report, User, Comment
from rides.models import Ride

router = Router(name='menu')


@router.message(F.text == "Забронировать поездку")
async def send_ride(message: types.Message, state: FSMContext):
    rides = Ride.objects.filter(departure__gte=timezone.now(), departure__lte=timezone.now() + timezone.timedelta(days=7))
    rides = rides.order_by('departure')
    rides = rides.values('departure').distinct()
    rides = [ride['departure'] for ride in rides]
    rides = [ride.strftime('%d.%m.%Y') for ride in rides]
    print(rides)
    await state.set_state(RideState.ride)
    if not rides:
        await message.answer(
            text='К сожалению, ближайших поездок нет.',
            reply_markup=types.ReplyKeyboardRemove()
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
    rides = Ride.objects.filter(departure=departure)
    rides = rides.order_by('departure')
    rides = rides.values('departure', 'ride_title')
    rides = [f"{ride['ride_title']} - {ride['departure'].strftime('%H:%M')}" for ride in rides]
    await state.set_state(RideState.confirm)
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


@router.message(RideState.confirm)
async def confirm_ride(message: types.Message, state: FSMContext):
    ride = Ride.objects.get(ride_title=message.text.split(' - ')[0])
    ride.user.add(message.from_user)
    await message.answer(
        text=f'Поездка {ride.ride_title} забронирована!',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(F.text == "Получить помощь")
async def get_help(message: types.Message, state: FSMContext):
    await state.set_state(ReportState.report)
    await message.answer(
        text='Введите ваше предложение:',
    )


@router.message(ReportState.report)
async def write_question(message: types.Message, state: FSMContext):
    user = User.objects.get(telegram_id=message.from_user.id)
    Report.objects.create(user=user, report=message.text)
    await message.answer(
        text='Ваше сообщение отправлено. Спасибо за обратную связь!',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(F.text == "Оставить отзыв/предложения")
async def send_comment(message: types.Message, state: FSMContext):
    await state.set_state(CommentState.comment)
    await message.answer(
        text='Введите ваш отзыв:',
    )


@router.message(CommentState.comment)
async def write_comment(message: types.Message, state: FSMContext):
    user = User.objects.get(telegram_id=message.from_user.id)
    Comment.objects.create(user=user, comment=message.text)
    await message.answer(
        text='Ваш отзыв отправлен. Спасибо за обратную связь!',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
