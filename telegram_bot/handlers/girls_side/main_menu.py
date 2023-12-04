from telegram_bot.loader import dp, bot
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
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_bot.loader import dp, bot
from telegram_bot.states import Survey, Initial
from telegram_bot.handlers.main_menu import main_bot_menu
from telegram_bot.service import girlsclub_db

from telegram_bot.assets.configs import config
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from telegram_bot.handlers.main_menu import create_keyboard_buttons


async def personal_cabinet(message: Message, state: FSMContext):
    buttons = create_keyboard_buttons('Посмотреть мероприятия', 'Мой реферальный код')
    await message.answer(f"Добро пожаловать в личный кабинет, {message.from_user.full_name}! Что вы хотите сделать?",
                         reply_markup=buttons)