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

from telegram_bot.loader import dp, bot
from telegram_bot.states import Survey
from telegram_bot.handlers.main_menu import create_keyboard_buttons


@dp.message(F.text == 'Зарегистрироваться')
async def start_survey(message: Message, state: FSMContext):
    await state.set_state(Survey.full_name)
    await message.answer("Введите ваше Имя:", reply_markup=ReplyKeyboardRemove())


@dp.message(Survey.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(Survey.age)
    await message.answer("Введите ваш возраст:")


@dp.message(Survey.age)
async def process_age(message: Message, state: FSMContext):
    ans = message.text
    if not ans.isdigit() or 0 < int(ans) < 100:
        await message.answer('Кажется, вы ввели возраст в неправильном формате!\n\n'
                             'Попробуйте, например, 18')
        return

    await state.update_data(age=int(message.text))
    await state.set_state(Survey.city)

    buttons = create_keyboard_buttons('Москва', 'Другой')

    await message.answer("Введите ваш город:", reply_markup=buttons)


@dp.message(Survey.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Survey.topics)
    await message.answer("Какие темы или области в жизни вы хотели бы "
                         "обсудить или изучить в рамках клуба?")


@dp.message(Survey.topics)
async def process_topics(message: Message, state: FSMContext):
    await state.update_data(topics=message.text)
    await state.set_state(Survey.goal)
    await message.answer("Какая основная цель вашего желания вступить в наш клуб?")


@dp.message(Survey.goal)
async def process_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await state.set_state(Survey.referral_code)

    buttons = create_keyboard_buttons('Пропустить')
    await message.answer("Если у вас есть реферальный код, то введите его:")


@dp.message(Survey.referral_code)
async def process_referral_code(message: Message, state: FSMContext):
    if message.text != 'Пропустить':
        '''Тут будет код для проверки на реферальный код'''
        await state.update_data(referral_code=message.text)
        pass

    data = await state.get_data()
    await message.answer(f"Спасибо за участие в опросе! Вот ваши данные:\n{data}", reply_markup=ReplyKeyboardRemove())
    await state.clear()
