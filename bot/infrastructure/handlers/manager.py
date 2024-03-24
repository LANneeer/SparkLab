from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from rides.models import Ride
from users.models import User, Comment

router = Router(name='manager_menu')


@router.message(F.text == "Просмотреть пользователей")
async def view_users(message: types.Message, state: FSMContext):
    if User.objects.get(telegram_id=message.from_user.id).is_admin:
        users = User.objects.all()
        users = [f"{user.username} - {user.first_name} {user.last_name}" for user in users]
        await message.answer(
            text='\n'.join(users),
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            text="У вас нет доступа к этой команде",
            reply_markup=types.ReplyKeyboardRemove()
        )


@router.message(F.text == "Просмотреть отзывы/предложения")
async def view_comments(message: types.Message, state: FSMContext):
    if User.objects.get(telegram_id=message.from_user.id).is_admin:
        comments = Comment.objects.all()
        comments = [f"{comment.user.username} - {comment.comment}" for comment in comments]
        await message.answer(
            text='\n'.join(comments),
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            text="У вас нет доступа к этой команде",
            reply_markup=types.ReplyKeyboardRemove()
        )


@router.message(F.text == "Просмотреть поездки")
async def view_rides(message: types.Message, state: FSMContext):
    if User.objects.get(telegram_id=message.from_user.id).is_admin:
        rides = Ride.objects.all()
        rides = [f"{ride.ride_title} - {ride.departure.strftime('%d.%m.%Y %H:%M')}" for ride in rides]
        await message.answer(
            text='\n'.join(rides),
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            text="У вас нет доступа к этой команде",
            reply_markup=types.ReplyKeyboardRemove()
        )
