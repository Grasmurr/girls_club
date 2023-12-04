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
from telegram_bot.service.girlsclub_db import update_event, get_all_event, get_event

import datetime


@dp.message(AdminMenu.manage_events, F.text == 'Редактировать мероприятие')
async def choose_event_to_edit(message: Message, state: FSMContext):
    events = await get_all_event()
    event_names = [event['name'] for event in events['data']]

    markup = create_keyboard_buttons(*event_names, 'Назад')
    await message.answer(text='Выберите мероприятие, которое вы хотите изменить',
                         reply_markup=markup)

    await state.set_state(AdminMenu.choose_event_to_edit)


@dp.message(AdminMenu.choose_event_to_edit)
async def choose_parameter_to_edit(message: Message, state: FSMContext):
    event_name = message.text
    if event_name == 'Назад':
        await manage_events(message, state)
        return

    events = await get_all_event()
    if event_name not in [event['name'] for event in events['data']] and event_name != "Отредактировать другой параметр":
        await message.answer("Событие не найдено. Попробуйте снова.")
        return

    markup = create_keyboard_buttons("Стоимость билетов",
                                     "Баннер", "Дата",
                                     "Описание", "Назад")

    await state.update_data(name=event_name)

    if event_name != "Отредактировать другой параметр":
        data = await state.get_data()
        event_name = data["name"]

    await message.answer(text=f'Выберите какой параметр мероприятия «{event_name}» вы хотите изменить',
                         reply_markup=markup)
    await state.set_state(AdminMenu.choose_parameter_to_edit)


@dp.message(AdminMenu.choose_parameter_to_edit, F.text == "Назад")
async def back_from_choose_parameter_to_edit(message: Message, state: FSMContext):
    await choose_event_to_edit(message, state)


@dp.message(AdminMenu.choose_parameter_to_edit)
async def enter_parameter_data(message: Message, state: FSMContext):
    parameter = message.text

    data = await state.get_data()
    event_name = data["name"]
    event_data = await get_event(event_name)
    price_for_new = event_data["price_for_new"]
    price_for_old = event_data["price_for_old"]
    event_date = event_data["event_date"]
    description = event_data['description']

    if parameter == "Стоимость билетов":
        markup = create_keyboard_buttons('Назад')
        await message.answer(f"На данный момент для мероприятия {event_name} установлены "
                             f"следующие цены билетов:\n\n"
                             f"Для новых участниц: {price_for_new}\n"
                             f"Для старых участниц: {price_for_old}\n\n"
                             f"Введите новые цены в столбик, сначала цену для "
                             f"новых участниц, потом для старых.", reply_markup=markup)
        await state.set_state(AdminMenu.edit_prices)

    elif parameter == "Дата":
        events = await get_all_event()

        data = await state.get_data()
        event_name = data["name"]

        markup = create_keyboard_buttons('Назад')
        await message.answer(f"На данный момент для мероприятия {event_name} "
                             f"установлена дата {event_date}. "
                             f"Пожалуйста, введите дату в формате YYYY-MM-DD. Например: 2023-10-29",
                             reply_markup=markup)
        await state.set_state(AdminMenu.edit_date)

    elif parameter == "Описание":
        markup = create_keyboard_buttons('Назад')
        await message.answer(f"На данный момент для мероприятия {event_name} "
                             f"установлено следующее описание:\n\n"
                             f"{description}\n\n"
                             f"Пожалуйста, пришлите новое описание", reply_markup=markup)
        await state.set_state(AdminMenu.edit_description)

    elif parameter == "Баннер":
        markup = create_keyboard_buttons('Назад')
        await message.answer(f"Пожалуйста, пришлите новый баннер для мероприятия {event_name}",
                             reply_markup=markup)
        await state.set_state(AdminMenu.edit_banner)

    else:
        await message.answer("Кажется, вы нажали не туда.")
        return


@dp.message(AdminMenu.edit_prices)
async def edit_prices(message: Message, state: FSMContext):
    prices = message.text.split("\n")
    if prices == 'Назад':
        await choose_parameter_to_edit(message, state)
        return

    price_for_new = int(prices[0])
    price_for_old = int(prices[1])

    data = await state.get_data()
    event_name = data["name"]

    markup = create_keyboard_buttons("Отредактировать другой параметр", 'Главное меню')
    await message.answer(f"Цены билетов для мероприятия «{event_name}» успешно изменены!\n\n"
                         f"Для новых участниц: {price_for_new}\n"
                         f"Для старых участниц: {price_for_old}\n\n", reply_markup=markup)
    await state.set_state(AdminMenu.after_editing)


@dp.message(AdminMenu.edit_date)
async def edit_date(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await choose_parameter_to_edit(message, state)
        return

    try:
        event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
        event_date_str = event_date.strftime('%Y-%m-%d')
        await state.update_data(event_date=event_date_str)
        markup = create_keyboard_buttons("Отредактировать другой параметр", 'Главное меню')
        await message.answer(f'Дата мероприятия изменена на {event_date_str}!', reply_markup=markup)

        data = await state.get_data()
        event_name = data["name"]
        await update_event(name=event_name, new_event_date=event_date_str)
        await state.set_state(AdminMenu.after_editing)

    except ValueError:
        await message.answer('Пожалуйста, введите дату в формате YYYY-MM-DD. Например: 2023-10-29')


@dp.message(AdminMenu.edit_description)
async def edit_description(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await choose_parameter_to_edit(message, state)
        return
    new_description = message.text
    data = await state.get_data()
    event_name = data["name"]
    await update_event(name=event_name, new_description=new_description)
    markup = create_keyboard_buttons("Отредактировать другой параметр", 'Главное меню')
    await message.answer(f'Описание мероприятия «{event_name}» успешно изменено!', reply_markup=markup)
    await state.set_state(AdminMenu.after_editing)


@dp.message(AdminMenu.edit_banner)
async def edit_banner(message: Message, state: FSMContext):
    if message.text == 'Назад':
        await choose_parameter_to_edit(message, state)
        return
    new_event_photo_id = message.text
    data = await state.get_data()
    event_name = data["name"]
    await update_event(name=event_name, new_event_photo_id=new_event_photo_id)
    markup = create_keyboard_buttons("Отредактировать другой параметр", 'Главное меню')
    await message.answer(f'Баннер мероприятия «{event_name}» успешно изменен!', reply_markup=markup)
    await state.set_state(AdminMenu.after_editing)


@dp.message(AdminMenu.after_editing)
async def after_editing(message: Message, state: FSMContext):
    if message.text == "Отредактировать другой параметр":
        await choose_parameter_to_edit(message, state)

    if message.text == 'Главное меню':
        await main_bot_menu(message, state)

