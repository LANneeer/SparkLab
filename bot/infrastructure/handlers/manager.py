from aiogram import Router, types, F

from bot.infrastructure.keyboards.default.manager import manager_menu
from bot.infrastructure.keyboards.default.user import user_menu
from rides.models import Ride
from users.models import User, Comment

router = Router(name='manager_menu')


@router.message(F.text == "Просмотреть пользователей")
async def view_users(message: types.Message):
    if User.objects.get(telegram_id=message.from_user.id).is_admin:
        users = User.objects.all()
        users = [f"t.me/{user.username} - {user.first_name} {user.last_name}" for user in users]
        if not users:
            users = ["Пользователей пока нет😔"]
        await message.answer(
            text='\n'.join(users),
            reply_markup=manager_menu
        )
    else:
        await message.answer(
            text="У вас нет доступа к этой команде❗",
            reply_markup=user_menu
        )


@router.message(F.text == "Просмотреть отзывы")
async def view_comments(message: types.Message):
    if User.objects.get(telegram_id=message.from_user.id).is_admin:
        comments = Comment.objects.all()
        comments = [f"t.me/{comment.user.username} - {comment.comment}" for comment in comments]
        if not comments:
            comments = ["Отзывов пока нет😔"]
        await message.answer(
            text='\n'.join(comments),
            reply_markup=manager_menu
        )
    else:
        await message.answer(
            text="У вас нет доступа к этой команде❗",
            reply_markup=user_menu
        )


@router.message(F.text == "Просмотреть поездки")
async def view_rides(message: types.Message):
    if User.objects.get(telegram_id=message.from_user.id).is_admin:
        rides = Ride.objects.all()
        rides = [f"{ride.ride_title} - {ride.departure.strftime('%d.%m.%Y %H:%M')}" for ride in rides]
        if not rides:
            rides = ["Поездок пока нет😔"]
        await message.answer(
            text='\n'.join(rides),
            reply_markup=manager_menu
        )
    else:
        await message.answer(
            text="У вас нет доступа к этой команде❗",
            reply_markup=user_menu
        )
