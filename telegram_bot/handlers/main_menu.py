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

from telegram_bot.service import girlsclub_db
from telegram_bot.states import Initial, PersonalCabinet


def create_keyboard_buttons(*args):
    builder = ReplyKeyboardBuilder()
    for i in args:
        builder.button(text=i)
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)


@dp.message(CommandStart())
async def main_bot_menu(message: Message, state: FSMContext):
    await state.set_state(Initial.initial)
    is_registered = await girlsclub_db.get_member_girl(message.from_user.id)

    if is_registered is None:
        markup = create_keyboard_buttons('Зарегистрироваться')
        await message.answer(text=f'Добро пожаловать в телеграм бот женского клуба! Для регистрации скорее'
                                  f'нажимай кнопку "Зарегистрироваться"',
                             reply_markup=markup)
    else:
        await personal_cabinet(message, state)


async def personal_cabinet(message: Message, state: FSMContext):
    await state.set_state(PersonalCabinet.initial)
    buttons = create_keyboard_buttons('Посмотреть мероприятия', 'Мой реферальный код')
    await message.answer(f"Добро пожаловать в личный кабинет, {message.from_user.full_name}! Что вы хотите сделать?",
                         reply_markup=buttons)
