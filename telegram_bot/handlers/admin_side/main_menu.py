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
from telegram_bot.states import Initial, AdminMenu, PersonalCabinet
from telegram_bot.handlers.main_menu import create_keyboard_buttons
from telegram_bot.assets.configs import config
from telegram_bot.handlers.main_menu import personal_cabinet

@dp.message(F.text == '/admin')
async def main_bot_menu(message: Message, state: FSMContext):
    if message.from_user.id == config.ADMIN_ID:
        await state.set_state(AdminMenu.initial)
        markup = create_keyboard_buttons('Управление мероприятиями',
                                         'Управление рассылкой',
                                         'Вернуться в кабинет участницы')
        await message.answer(text=f'Добро пожаловать в админ панель женского клуба!',
                             reply_markup=markup)
    else:
        await message.answer('Кажется, вы не являетесь админом!')


@dp.message(AdminMenu.initial, F.text == 'Вернуться в кабинет участницы')
async def back_to_personal_cabinet(message: Message, state: FSMContext):
    await personal_cabinet(message, state)