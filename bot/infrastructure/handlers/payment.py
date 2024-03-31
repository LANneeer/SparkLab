from aiogram import Router, types, F

from rides.models import RideRequest

router = Router(name='payment')


@router.callback_query(F.data.startswith('confirm'))
async def confirm_ride(call: types.CallbackQuery):
    ride = RideRequest.objects.get(id=call.data.split('_')[1])
    user = ride.user
    if ride.status == 'pending':
        ride.status = 'approved'
        ride.save()
        await call.bot.send_message(
            chat_id=user.telegram_id,
            text=f'Ваша поездка {ride.ride.ride_title} к {ride.ride.departure.strftime("%d.%m.%Y %H:%M")} подтверждена.'
        )
        await call.answer('Поездка подтверждена')
    else:
        await call.answer(f'Поездка уже {ride.status}')


@router.callback_query(F.data.startswith('decline'))
async def decline_ride(call: types.CallbackQuery):
    ride = RideRequest.objects.get(id=call.data.split('_')[1])
    user = ride.user
    if ride.status == 'pending':
        ride.status = 'rejected'
        ride.save()
        await call.bot.send_message(
            chat_id=user.telegram_id,
            text=f'Ваша поездка {ride.ride.ride_title} к {ride.ride.departure.strftime("%d.%m.%Y %H:%M")} отклонена.'
        )
        await call.answer('Поездка отклонена')
    else:
        await call.answer(f'Поездка уже {ride.status}')


# TODO: add ride canceling
