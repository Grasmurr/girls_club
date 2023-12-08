from telegram_bot.loader import dp, bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import \
    (Message,
     CallbackQuery,
     KeyboardButton,
     ReplyKeyboardMarkup,
     InlineKeyboardMarkup,
     InlineKeyboardButton,
     ReplyKeyboardRemove
     )
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import BufferedInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from aiogram.enums.content_type import ContentType

from telegram_bot.service import girlsclub_db
from telegram_bot.states import Initial, AdminMenu
from telegram_bot.handlers.main_menu import create_keyboard_buttons
from telegram_bot.assets.configs import config
from telegram_bot.handlers.admin_side.main_menu import main_bot_menu
from telegram_bot.handlers.admin_side.manage_events import manage_events
from telegram_bot.handlers.helpers import chat_backends
from telegram_bot.service.girlsclub_db import create_event

import datetime






@dp.message(AdminMenu.manage_events, F.text == 'Создать мероприятие')
async def create_new_event(message: Message, state: FSMContext):
    markup = create_keyboard_buttons('Назад')
    await message.answer(text='Введите название мероприятия',
                         reply_markup=markup)

    await state.set_state(AdminMenu.enter_event_name)

@dp.message(AdminMenu.enter_event_name, F.text == 'Назад')
async def back_form_create_new_event(message: Message, state: FSMContext):
    await manage_events (message, state)


@dp.message(AdminMenu.enter_event_name)
async def enter_event_name(message: Message, state: FSMContext):
    name_of_event = message.text
    markup = chat_backends.create_keyboard_buttons('Да', 'Назад')
    await message.answer(f'Вы хотите создать мероприятие «{name_of_event}». Продолжить?',
                         reply_markup=markup)
    await state.update_data(name=name_of_event)
    await state.set_state(AdminMenu.confirm_event_name)


@dp.message(AdminMenu.confirm_event_name)
async def question_continue_create_event(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await create_new_event(message, state)
    else:
        await message.answer(text=f'Пожалуйста, введите дату в '
                                  f'формате YYYY-MM-DD. Например: 2023-10-29',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(AdminMenu.enter_date_of_event)


@dp.message(AdminMenu.enter_date_of_event)
async def create_event_date(message: Message, state: FSMContext):
    try:
        event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
        event_date_str = event_date.strftime('%Y-%m-%d')
        await state.update_data(event_date=event_date_str)

        await message.answer(f'Дата мероприятия установлена на {event_date_str}\n\n'
                             f'Теперь пришлите, пожалуйста, баннер мероприятия')
        await state.set_state(AdminMenu.upload_photo_of_event)

    except ValueError:

        await message.answer('Пожалуйста, введите дату в формате YYYY-MM-DD. Например: 2023-10-29')


@dp.message(AdminMenu.upload_photo_of_event, F.photo)
async def create_banner_of_event(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    print(photo_id)
    await state.update_data(mailing_type='Фото', photo_id=photo_id)

    buttons = chat_backends.create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите установить эту фотографию на баннер?', reply_markup=buttons)
    await message.answer_photo(photo=photo_id)
    await state.set_state(AdminMenu.confirm_event_banner)


@dp.message(AdminMenu.upload_photo_of_event, F.document)
async def wrong_banner_of_event(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте фотографию быстрым способом, не файлом')


@dp.message(AdminMenu.upload_photo_of_event, F.text)
async def text_instead_banner_of_event(message: Message, state: FSMContext):
    await message.answer('Кажется вы нажали не туда')


@dp.message(AdminMenu.confirm_event_banner, F.text == 'Назад')
async def back_from_banner_of_event(message: Message, state: FSMContext):
    await create_event_date(message, state)


@dp.message(AdminMenu.confirm_event_banner, F.text == 'Подтвердить')
async def enter_description_of_event(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, пришлите описание мероприятия", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AdminMenu.enter_description_of_event)


@dp.message(AdminMenu.enter_description_of_event)
async def confirm_description_of_event(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    markup = chat_backends.create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer(f"Вы установили следующее описание для мероприятия: \n\n"
                         f"{description}\n\n"
                         f"Продолжить?", reply_markup=markup)
    await state.set_state(AdminMenu.confirm_description_of_event)


@dp.message(AdminMenu.confirm_description_of_event, F.text == 'Назад')
async def back_from_confirm_description_of_event(message: Message, state: FSMContext):
    await enter_description_of_event(message, state)


@dp.message(AdminMenu.confirm_description_of_event, F.text == 'Подтвердить')
async def enter_new_girl_price(message: Message, state: FSMContext):
    await message.answer("Введите цифрой стоимость билета для "
                         "новых участников (без кода подруги)")
    await state.set_state(AdminMenu.enter_new_girl_price)


@dp.message(AdminMenu.enter_new_girl_price)
async def enter_old_girl_price(message: Message, state: FSMContext):
    new_girl_price = int(message.text)
    await state.update_data(new_girl_price=new_girl_price)
    await message.answer("Введите цифрой стоимость билета для "
                         "старых участников (со скидкой)")
    await state.set_state(AdminMenu.enter_old_girl_price)


@dp.message(AdminMenu.enter_old_girl_price)
async def enter_old_girl_price(message: Message, state: FSMContext):
    old_girl_price = int(message.text)
    await state.update_data(old_girl_price=old_girl_price)
    data = await state.get_data()
    new_girl_price = data['new_girl_price']
    markup = chat_backends.create_keyboard_buttons('Продолжить', 'Ввести стоимость билетов заново')
    await message.answer(f'Вы установили следующие стоимости билетов:\n\n'
                         f'Для новых участниц: {new_girl_price}\n'
                         f'Для старых участниц: {old_girl_price}\n\n'
                         f'Продолжить?', reply_markup=markup)
    await state.set_state(AdminMenu.confirm_prices)


@dp.message(AdminMenu.confirm_prices, F.text == 'Продолжить')
async def upload_ticket_photo(message: Message, state: FSMContext):
    await message.answer('Пожалуйста пришлите макет билета')
    await state.set_state(AdminMenu.upload_ticket_photo)


@dp.message(AdminMenu.confirm_prices, F.text == 'Ввести стоимость билетов заново')
async def rewrite_prices(message: Message, state: FSMContext):
    await enter_new_girl_price(message, state)


@dp.message(AdminMenu.upload_ticket_photo, F.photo)
async def get_ticket_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(mailing_type='Фото билета', ticket_photo_id=photo_id)

    await message.answer("Мероприятие зарегистрировано!")

    data = await state.get_data()
    print(data['ticket_photo_id'], "АААААААААА")
    await create_event(
        name=data['name'],
        price_for_new=data['new_girl_price'],
        price_for_old=data['old_girl_price'],
        event_photo_id=data['photo_id'],
        ticket_photo_id=data['ticket_photo_id'],
        description=data['description'],
        event_date=data['event_date']
    )

    await main_bot_menu(message, state)
