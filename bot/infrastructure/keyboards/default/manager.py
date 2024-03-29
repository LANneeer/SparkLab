from aiogram import types

manager_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='Просмотреть пользователей')
        ],
        [
            types.KeyboardButton(text='Просмотреть отзывы')
        ],
        [
            types.KeyboardButton(text='Просмотреть поездки')
        ]
    ],
    resize_keyboard=True
)
