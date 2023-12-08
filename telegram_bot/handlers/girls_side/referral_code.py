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


@dp.message(PersonalCabinet.girls_menu, F.text == 'Мой реферальный код')
async def send_referral_code(message: Message, state: FSMContext):
    await message.answer("Ваш реферальный код — GHF4839\n\n"
                         "Поделитесь им с подругой, которую хотите пригласить в клуб")
