import re

from aiogram.types import \
    (Message,
     CallbackQuery,
     KeyboardButton,
     ReplyKeyboardMarkup,
     InlineKeyboardMarkup,
     InlineKeyboardButton,
     ReplyKeyboardRemove
     )
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_bot.loader import dp, bot
from telegram_bot.states import Survey, Initial
from telegram_bot.handlers.main_menu import main_bot_menu
from telegram_bot.service import girlsclub_db

from telegram_bot.assets.configs import config
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from telegram_bot.handlers.main_menu import personal_cabinet
from telegram_bot.states import PersonalCabinet
from telegram_bot.service.girlsclub_db import get_all_event, get_event, get_member_girl
from telegram_bot.handlers.main_menu import create_keyboard_buttons

import datetime
import locale
import calendar


@dp.message(PersonalCabinet.girls_menu, F.text == 'Афиша мероприятий')
async def choose_event_to_show(message: Message, state: FSMContext):
    events = await get_all_event()
    event_names = [event['name'] for event in events['data']]

    markup = create_keyboard_buttons(*event_names, 'Назад')
    await message.answer("Для того, чтобы получить информацию о мероприятии,"
                         " выберите название из кнопок ниже",
                         reply_markup=markup)
    await state.set_state(PersonalCabinet.choose_event_to_show)


async def normalize_date(date):

    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    eng_formatted_date = date_obj.strftime('%d %B %Y')

    day, month, year = eng_formatted_date.split()

    month_index = list(calendar.month_name).index(month)

    month_name_ru = calendar.month_name[month_index].lower()

    formatted_date = f"{day} {month_name_ru} {year}"

    return formatted_date


async def choose_price_for_user(user_id, price_for_new, price_for_old):
    girl_data = await get_member_girl(user_id)
    girl_status = girl_data["old_or_new"]  # здесь возможно есть ошибка
    if girl_status == 'old':
        price = int(price_for_old)
    else:
        price = int(price_for_new)
    return price


@dp.message(PersonalCabinet.choose_event_to_show)
async def show_event_data(message: Message, state: FSMContext):
    event_name = message.text
    user_id = message.from_user.id

    events = await get_all_event()
    event_names = [event['name'] for event in events['data']]
    if event_name not in event_names and event_name != "Назад":
        await message.answer("Кажется, такого мероприятия не существует! "
                             "Для выбора мероприятия воспользуйтесь кнопками ниже")
        return

    elif event_name == "Назад":
        await personal_cabinet(message, state)

    else:
        event_data = await get_event(event_name)
        price_for_new = event_data["price_for_new"]
        price_for_old = event_data["price_for_old"]
        event_photo_id = event_data["event_photo_id"]
        ticket_photo_id = event_data["event_photo_id"]
        description = event_data['description']
        event_date = await normalize_date(event_data["event_date"])

        price = await choose_price_for_user(user_id, price_for_new, price_for_old)

        await state.update_data(event_name=event_name,
                                price=price,
                                event_photo_id=event_photo_id,
                                ticket_photo_id=ticket_photo_id,
                                description=description,
                                event_date=event_date)

        data = await state.get_data()

        markup = create_keyboard_buttons("Посмотреть другие мероприятия", "Вернуться в основное меню")
        caption = (f"<b>{event_name}</b>\n\n"
                   f"<b>Когда?</b> {event_date}\n\n"
                   f"{description}\n\n"
                   f"<b>Стоимость билета:</b> {price} рублей\n\n"
                   f"<b>Нажимай на кнопку ниже, чтобы присоединиться к мероприятию</b>")
        await message.answer_photo(photo=event_photo_id,
                                   caption=caption,
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=markup)
        # TODO: добавить инлайн на оплату
        await state.set_state(PersonalCabinet.after_show_one_event)


@dp.message(PersonalCabinet.after_show_one_event)
async def after_show_one_event(message: Message, state: FSMContext):
    action = message.text

    if action == "Посмотреть другие мероприятия":
        await choose_event_to_show(message, state)

    elif action == "Вернуться в основное меню":
        await personal_cabinet(message, state)

    else:
        await message.answer("Кажется, вы нажали не на кнопку!")
        return
