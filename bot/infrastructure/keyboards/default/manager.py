from aiogram import types

manager_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='Забронировать поездку')
        ],
        [
            types.KeyboardButton(text='Мои поездки')
        ],
        [
            types.KeyboardButton(text='Получить помощь')
        ],
        [
            types.KeyboardButton(text='Оставить отзыв/предложения')
        ]
    ],
    resize_keyboard=True
)


