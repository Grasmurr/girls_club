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


@dp.message(AdminMenu.initial, F.text == 'Управление мероприятиями')
async def manage_events(message: Message, state: FSMContext):
    markup = create_keyboard_buttons('Создать мероприятие',
                                     "Редактировать мероприятие",
                                     'Скрыть/показать мероприятие',
                                     'Назад')
    await state.set_state(AdminMenu.manage_events)
    await message.answer(text='Что вы хотите сделать?',
                         reply_markup=markup)


@dp.message(AdminMenu.manage_events, F.text == 'Назад')
async def back(message: Message, state: FSMContext):
    await main_bot_menu(message, state)

