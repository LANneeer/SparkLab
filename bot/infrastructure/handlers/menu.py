from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.infrastructure.states.main import Main

router = Router()


@router.message(Command("menu"))
async def menu(message: types.Message):
    await message.answer(
        text='<b>Меню</b>',
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text='Получить помощь')
                ],
                [
                    types.KeyboardButton(text='Узнать о загруженности общественного транспорта')
                ],
                [
                    types.KeyboardButton(text='Сообщить о загруженности общественного транспорта')
                ],
                [
                    types.KeyboardButton(text='Оставить отзыв/предложения')
                ]
            ],
            resize_keyboard=True
        )
    )


@router.message("Получить помощь")
async def get_help(message: types.Message):
    await message.answer(
        text='<b>Степени загруженности:</b>\n'
             '/level1 - Минимум людей, много мест\n'
             '/level2 - Небольшая загруженность, есть свободные места\n'
             '/level3 - Много людей, ограниченные места, дискомфорт'
    )


@router.message("Узнать о загруженности общественного транспорта")
async def get_crowd(message: types.Message):
    await message.answer(
        text="some data"
    )


@router.message("Сообщить о загруженности общественного транспорта")
@router.message(Command("report"))
async def report(message: types.Message, state: FSMContext):
    await state.set_state(Main.report)
    await message.answer(
        text='Введите ваш отзыв/предложение:',
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text='🟢 level1')
                ],
                [
                    types.KeyboardButton(text='🟡 level2')
                ],
                [
                    types.KeyboardButton(text='🔴 level3')
                ],
            ],
            resize_keyboard=True
        )
    )


@router.message(Main.report)
async def passing_data(message: types.Message, state: FSMContext):
    await state.update_data(report=message.text)
    await state.set_state(Main.confirm)
    await message.answer(text=f'Ваше сообщение: {message.text}\n'
                              'Подтвердите отправку',
                         reply_markup=types.ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     types.KeyboardButton(text='Отправить')
                                 ],
                                 [
                                     types.KeyboardButton(text='Отменить')
                                 ]
                             ],
                             resize_keyboard=True
                         )
                         )
