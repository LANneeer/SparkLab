from aiogram.fsm.state import State, StatesGroup


class Main(StatesGroup):
    menu = State()
    report = State()
    confirm = State()


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
