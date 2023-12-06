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
from telegram_bot.states import Survey, Initial, PersonalCabinet
from telegram_bot.handlers.main_menu import create_keyboard_buttons
from telegram_bot.handlers.main_menu import main_bot_menu
from telegram_bot.service import girlsclub_db

from telegram_bot.assets.configs import config


@dp.message(Initial.initial, F.text == 'Зарегистрироваться')
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
    if not ans.isdigit() or not 0 < int(ans) < 100:
        await message.answer('Кажется, вы ввели возраст в неправильном формате!\n\n'
                             'Попробуйте, например, 18')
        return
    await state.update_data(age=int(message.text))
    await state.set_state(Survey.city)
    buttons = create_keyboard_buttons('Москва', 'Другой')
    await message.answer("Введите ваш город:", reply_markup=buttons)


@dp.message(Survey.city)
async def process_city(message: Message, state: FSMContext):
    ans = message.text
    if ans != 'Москва':
        await message.answer('К сожалению, мы работаем только в Москве')
        await main_bot_menu(message, state)
        return

    await state.update_data(city=message.text)
    await state.set_state(Survey.topics)
    await message.answer("Какие темы или области в жизни вы хотели бы "
                         "обсудить или изучить в рамках клуба?", reply_markup=ReplyKeyboardRemove())


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
    await message.answer("Если у вас есть реферальный код, то введите его:",
                         reply_markup=buttons)


@dp.message(Survey.referral_code)
async def process_referral_code(message: Message, state: FSMContext):
    if message.text != 'Пропустить':
        # TODO: '''Тут будет код для проверки на реферальный код'''
        await state.update_data(referral_code=message.text)
        old_or_new = "old"

    else:
        old_or_new = "new"

    print ("ПЕЧАТАЮ  ", old_or_new)
    await state.update_data(old_or_new=old_or_new)
    data = await state.get_data()
    print ("ПЕЧАТАЮ  ", data['old_or_new'])


    data = await state.get_data()
    await message.answer(f"Спасибо за заполнение анкеты! Вот ваши данные:\n\n"
                         f"Имя: {data['full_name']}\nВозраст: {data['age']}\nТемы для обсуждения: "
                         f"{data['topics']}\nВаша цель: {data['goal']}\n\nВ скором времени мы "
                         f"рассмотрим вашу заявку!")
    builder = InlineKeyboardBuilder()
    builder.button(text='Подтвердить', callback_data=f'allow{message.from_user.id}')
    builder.button(text='Отказать', callback_data=f'decline{message.from_user.id}')
    markup = builder.as_markup()

    await bot.send_message(chat_id=config.ADMIN_ID,
                           text=f"Поступила новая заявка на вступление!\nДанные кандидатки:"
                                f"\n\nИмя: {data['full_name']}\nВозраст: {data['age']}\n"
                                f"Темы для обсуждения: {data['topics']}\nЦель кандидатки: {data['goal']}",
                           reply_markup=markup)
    # await state.clear()


@dp.callback_query(lambda call: call.data.startswith('allow') or call.data.startswith('decline'))
async def handle_admin_decision(call: CallbackQuery, state: FSMContext):
    ans = call.data
    user_id = ans[5:]

    if ans[:5] == 'allow':
        text = call.message.text

        pattern = r"Имя: (?P<full_name>.+)\nВозраст: (?P<age>\d+)\nТемы для обсуждения: " \
                  r"(?P<topics>.+)\nЦель кандидатки: (?P<goal>.+)"

        match = re.search(pattern, text)

        if match:
            data = match.groupdict()
            data['age'] = int(data['age'])
        else:
            data = None

        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text=f'Вы подтвердили заявку участницы '
                                                                  f'{data["full_name"]}!')
        data = await state.get_data()
        await girlsclub_db.create_member_girl(telegram_id=user_id,
                                              full_name=data['full_name'],
                                              age=data['age'],
                                              unique_id='BOL123',
                                              discussion_topics=data['topics'],
                                              joining_purpose=data['goal'],
                                              old_or_new=data["old_or_new"])
        # TODO: Обсудить, как будут создаваться уникальные id

        await bot.send_message(chat_id=user_id, text='Админ подтвердил вашу заявку!')
        await state.set_state(PersonalCabinet.girls_menu)
        markup = create_keyboard_buttons('Афиша мероприятий', 'Мой реферальный код')
        await bot.send_message(chat_id=user_id,
                               text=f'Добро пожаловать в личный кабинет! Что вы хотите посмотреть?',
                               reply_markup=markup)



    else:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id, text='Вы отказали в заявке представителю!')
        await bot.send_message(chat_id=ans[7:], text='Админ отказал вам в заявке!')
        markup = create_keyboard_buttons('Зарегистрироваться')
        await state.set_state(Initial.initial)
        await bot.send_message(chat_id=ans[7:],
                               text=f'Добро пожаловать в телеграм бот женского клуба! '
                                    f'Для регистрации скорее'
                                    f'нажимай кнопку "Зарегистрироваться"',
                               reply_markup=markup)