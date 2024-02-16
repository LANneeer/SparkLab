from aiogram.fsm.state import State, StatesGroup


class Main(StatesGroup):
    menu = State()
    report = State()
    confirm = State()


class Registration(StatesGroup):
    report = State()
    confirm = State()
