from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.infrastructure.keyboards.default.user import user_menu
from bot.infrastructure.states.main import CommentState
from rides.models import RideRequest
from users.models import User, Comment

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
            text=f'Ваша поездка {ride.ride.ride_title} к {ride.ride.departure.strftime("%d.%m.%Y %H:%M")} подтверждена.\n' \
                 f'Ваша поездка от KBTU DORM до KBTU успешно подтверждена!\n' \
                 f'Пожалуйста, будьте внимательны к времени и не опаздывайте на шаттл, который подъедет к вам с улицы Ислама Каримова. Рекомендуем быть на месте за 5-10 минут до отправления.\n' \
                 f'Обратите внимание, что мы не несем ответственности, если вы опоздаете на поездку.\n' \
                 f'Пожалуйста, помните, что возврат оплаты возможен при отмене более чем за 12 часов до поездки, но мы также рассматриваем все случаи индивидуально.\n' \
                 f'Если у вас возникнут какие-либо вопросы или проблемы, не стесняйтесь обращаться к команде /help.\n' \
                 f'Желаем вам приятной поездки и благодарим за доверие к нам!🚀\n\n' \
                 f'Пожалуйста подтвердите что вы сели на место нажав на кнопку "Я на месте" внизу сообщения.',
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(text='Я на месте', callback_data=f'arrived_{ride.id}')
                    ]
                ]
            )
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


@router.callback_query(F.data.startswith('arrived'))
async def arrived_ride(call: types.CallbackQuery):
    ride = RideRequest.objects.get(id=call.data.split('_')[1])
    user = ride.user
    if ride.status == 'approved':
        ride.status = 'arrived'
        ride.save()
        await call.bot.send_message(
            chat_id=user.telegram_id,
            text=f'Спасибо за подтверждение! Приятной поездки!\n\n' \
                 f'Пожалуйста, не забудьте поделиться своими впечатлениями о поездке с нами, чтобы мы могли улучшить наш сервис.',
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(text='Оставить отзыв', callback_data='leave_review')
                    ]
                ]
            )
        )
    else:
        await call.answer(f'Поездка уже {ride.status}')


@router.callback_query(F.data == 'leave_review')
async def leave_review(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        text='Оставьте ваш отзыв о поездке:',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(CommentState.comment)
    await call.answer()


@router.message(CommentState.comment)
async def review(message: types.Message, state: FSMContext):
    Comment.objects.create(
        user=User.objects.get(telegram_id=message.from_user.id),
        comment=message.text
    )
    await message.answer(
        text='Спасибо за ваш отзыв! Ваше мнение очень важно для нас.',
        reply_markup=user_menu
    )
    await state.clear()
