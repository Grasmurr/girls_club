from aiogram.fsm.state import StatesGroup, State


class Survey(StatesGroup):
    full_name = State()
    age = State()
    city = State()
    topics = State()
    goal = State()
    referral_code = State()


class PersonalCabinet(StatesGroup):
    initial = State()


class AdminMenu(StatesGroup):
    initial = State()

