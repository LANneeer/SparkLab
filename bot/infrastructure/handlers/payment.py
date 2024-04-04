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
            text=f'Ваша поездка {ride.ride.ride_title} к {ride.ride.departure.strftime("%d.%m.%Y %H:%M")} подтверждена.' \
                 f'Ваша поездка от KBTU DORM до KBTU успешно подтверждена!' \
                 f'Пожалуйста, будьте внимательны к времени и не опаздывайте на шаттл, который подъедет к вам с улицы Ислама Каримова. Рекомендуем быть на месте за 5-10 минут до отправления.' \
                 f'Обратите внимание, что мы не несем ответственности, если вы опоздаете на поездку.' \
                 f'Пожалуйста, помните, что возврат оплаты возможен при отмене более чем за 12 часов до поездки, но мы также рассматриваем все случаи индивидуально.' \
                 f'Если у вас возникнут какие-либо вопросы или проблемы, не стесняйтесь обращаться к команде /help.' \
                 f'Желаем вам приятной поездки и благодарим за доверие к нам!'
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
