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


def create_keyboard_buttons(*args):
    builder = ReplyKeyboardBuilder()
    for i in args:
        builder.button(text=i)
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)


@dp.message(CommandStart())
async def main_bot_menu(message: Message, state: FSMContext):

    markup = create_keyboard_buttons('Зарегистрироваться')

    # is_registered = await api_methods.get_promouter(message.from_user.id)

    # print(is_registered)

    # if is_registered and len(is_registered['data']) != 0:
    #     await main_promouter_panel.accepted_promouter_panel(message, state)
    # else:
    #     await state.set_state(PromouterStates.begin_registration)
    await message.answer(text=f'Добро пожаловать в телеграм бот женского клуба! ',
                         reply_markup=markup)