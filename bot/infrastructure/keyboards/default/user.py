from aiogram import types

user_menu = types.ReplyKeyboardMarkup(
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
            types.KeyboardButton(text='Оставить отзыв')
        ]
    ],
    resize_keyboard=True
)
