from aiogram.fsm.state import State, StatesGroup


class MenuState(StatesGroup):
    menu = State()


class ReportState(StatesGroup):
    report = State()
    confirm = State()


class CommentState(StatesGroup):
    comment = State()
    confirm = State()


class RideState(StatesGroup):
    ride = State()
    payment = State()
    confirm = State()



class RegistrationState(StatesGroup):
    first_name = State()
    last_name = State()
