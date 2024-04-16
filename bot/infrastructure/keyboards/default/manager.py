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
        ],
        [
            types.KeyboardButton(text='Посмотреть записи')
        ]
    ],
    resize_keyboard=True
)
