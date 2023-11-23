from aiogram.fsm.state import StatesGroup, State


class Initial(StatesGroup):
    initial = State()


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
    manage_events = State()
    enter_event_name = State()
    delete_event = State()
    confirm_event_name = State()

    manage_mailing = State()
    handle_mailing = State()
    delete_mailing = State()

    moment_mailing = State()
    mailing_with_text = State()
    mailing_with_photo = State()
    mailing_with_file = State()

