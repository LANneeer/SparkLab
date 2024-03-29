from aiogram import Router, types, F

from users.models import User

router = Router(name='payment')


@router.callback_query(F.data.startswith('confirm'))
async def confirm_ride(call: types.CallbackQuery):
    user = User.objects.get(id=call.data.split('_')[1])
    ride = user.rides.first()
    await call.bot.send_message(
        chat_id=user.telegram_id,
        text=f'Ваша поездка {ride.ride_title} на {ride.departure.strftime("%d.%m.%Y %H:%M")} подтверждена.'
    )
    await call.answer('Поездка подтверждена')


@router.callback_query(F.data.startswith('decline'))
async def decline_ride(call: types.CallbackQuery):
    user = User.objects.get(id=call.data.split('_')[1])
    ride = user.rides.first()
    await call.bot.send_message(
        chat_id=user.telegram_id,
        text=f'Ваша поездка {ride.ride_title} на {ride.departure.strftime("%d.%m.%Y %H:%M")} отклонена.'
    )
    await call.answer('Поездка отклонена')
