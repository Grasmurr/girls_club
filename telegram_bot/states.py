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
    enter_date_of_event = State()
    upload_photo_of_event = State()
    delete_event = State()
    confirm_event_name = State()
    confirm_event_banner = State()
    enter_description_of_event = State()
    confirm_description_of_event = State()
    enter_new_girl_price = State()
    enter_old_girl_price = State()
    confirm_prices = State()
    upload_ticket_photo = State()

    choose_event_to_edit = State()
    choose_parameter_to_edit = State()
    edit_prices = State()
    confirm_edited_prices = State()
    edit_date = State()
    edit_description = State()
    edit_banner = State()
    after_editing = State()

    manage_mailing = State()
    handle_mailing = State()
    delete_mailing = State()

    moment_mailing = State()
    mailing_with_text = State()
    mailing_with_photo = State()
    mailing_with_file = State()

