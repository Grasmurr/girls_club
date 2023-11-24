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

from telegram_bot.service import girlsclub_db
from telegram_bot.states import Initial, AdminMenu
from telegram_bot.handlers.main_menu import create_keyboard_buttons
from telegram_bot.assets.configs import config
from telegram_bot.handlers.admin_side.main_menu import main_bot_menu
from telegram_bot.handlers.admin_side.manage_events import create_new_event
from telegram_bot.helpers import chat_backends


import datetime

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

@dp.message(AdminMenu.enter_date_of_event, F.photo)
async def create_banner_of_event(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(mailing_type='Фото', photo_id=photo_id)
    buttons = chat_backends.create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите установить эту фотографию на баннер?', reply_markup=buttons)
    await message.answer_photo(photo=photo_id)
