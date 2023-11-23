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
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_bot.service import girlsclub_db
from telegram_bot.states import Initial, AdminMenu
from telegram_bot.handlers.main_menu import create_keyboard_buttons
from telegram_bot.assets.configs import config
from telegram_bot.handlers.admin_side.main_menu import main_bot_menu


@dp.message(AdminMenu.initial, F.text == 'Управление рассылкой')
async def manage_mailing(message: Message, state: FSMContext):
    markup = create_keyboard_buttons('Регулярная рассылка',
                                     'Удалить регулярную рассылку',
                                     'Рассылка в моменте',
                                     'Назад')
    await state.set_state(AdminMenu.manage_mailing)
    await message.answer(text='Что вы хотите сделать?',
                         reply_markup=markup)


@dp.message(AdminMenu.manage_mailing, F.text == 'Регулярная рассылка')
async def create_or_change_mailing(message: Message, state: FSMContext):
    buttons = create_keyboard_buttons('Назад')
    await message.answer(text='Хорошо! Отправьте фото (с подписью) для новой рассылки:',
                         reply_markup=buttons)
    await state.set_state(AdminMenu.handle_mailing)


@dp.message(AdminMenu.handle_mailing, F.text == 'Назад')
async def back(message: Message, state: FSMContext):
    await manage_mailing(message, state)


@dp.message(AdminMenu.manage_mailing, F.text == 'Удалить регулярную рассылку')
async def delete_mailing(message: Message, state: FSMContext):
    newsletter = await girlsclub_db.get_newsletter(number=1)
    if newsletter is not None:
        builder = InlineKeyboardBuilder()
        builder.button(text='Удалить', callback_data=f'delete_newsletter')
        builder.button(text='Отмена', callback_data=f'cancel_deletting')
        markup = builder.as_markup()
        await message.answer(text='Вы хотите удалить эту регулярную рассылку?')
        await message.answer_photo(photo=newsletter['photo_id'], caption=newsletter['text'], reply_markup=markup)
    else:
        await message.answer('Кажется, вы еще не создали регулярную рассылку!')


@dp.callback_query(lambda call: call.data in ['delete_newsletter', 'cancel_deletting'])
async def handle_admin_decision(call: CallbackQuery, state: FSMContext):
    ans = call.data
    if ans == 'delete_newsletter':
        await girlsclub_db.delete_newsletter(1)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Вы успешно удалили ежедневную рассылку!')
        await state.set_state(AdminMenu.initial)
        markup = create_keyboard_buttons('Управление мероприятиями',
                                         'Управление рассылкой',
                                         'Вернуться в кабинет участницы')
        await bot.send_message(chat_id=call.message.chat.id, text=f'Добро пожаловать в админ панель женского клуба!',
                               reply_markup=markup)

    else:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.message.chat.id,
                               text='Вы отменили удаление рассылки!')
        await state.set_state(AdminMenu.initial)
        markup = create_keyboard_buttons('Управление мероприятиями',
                                         'Управление рассылкой',
                                         'Вернуться в кабинет участницы')
        await bot.send_message(chat_id=call.message.chat.id, text=f'Добро пожаловать в админ панель женского клуба!',
                               reply_markup=markup)


@dp.message(AdminMenu.delete_mailing, F.text == 'Подтвердить')
async def back(message: Message, state: FSMContext):
    await girlsclub_db.delete_newsletter(number=1)
    await message.answer('Вы удалили эту рассылку!')


@dp.message(AdminMenu.manage_mailing, F.text == 'Назад')
async def back(message: Message, state: FSMContext):
    await main_bot_menu(message, state)


@dp.message(AdminMenu.handle_mailing, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    caption = message.caption
    await state.update_data(mailing_type='Фото', photo_id=photo_id, caption=caption)
    buttons = create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите расслылать это фото с такой подписью?', reply_markup=buttons)
    await message.answer_photo(photo=photo_id, caption=caption)


@dp.message(AdminMenu.handle_mailing, F.text == 'Подтвердить')
async def start_photo_mailing(message: Message, state: FSMContext):
    data = await state.get_data()
    await girlsclub_db.create_or_update_newsletter(number=1, photo_id=data['photo_id'], text=data['caption'])
    await message.answer('Хорошо! Вы установили эту рассылку на ежедневную основу!')
    await main_bot_menu(message, state)


@dp.message(AdminMenu.handle_mailing, F.text == 'Назад')
async def start_photo_mailing(message: Message, state: FSMContext):
    await manage_mailing(message, state)


@dp.message(AdminMenu.manage_mailing, F.text == 'Рассылка в моменте')
async def moment_mailing(message: Message, state: FSMContext):
    buttons = create_keyboard_buttons('Текст', 'Фото', 'Файл', 'Назад')
    await message.answer('Хорошо! Выберите в каком формате вы хотите отправить рассылку:',
                         reply_markup=buttons)
    await state.set_state(AdminMenu.moment_mailing)


@dp.message(AdminMenu.moment_mailing, F.text == 'Назад')
async def back_to_admin_menu(message: Message, state: FSMContext):
    await manage_mailing(message, state)


@dp.message(AdminMenu.moment_mailing)
async def back_to_admin_menu(message: Message, state: FSMContext):
    type_to_mail = message.text
    if type_to_mail not in ['Текст', 'Фото', 'Файл']:
        buttons = create_keyboard_buttons('Текст', 'Фото', 'Файл', 'Назад')
        await message.answer('Кажется, вы выбрали что-то не из кнопок. Пожалуйста, воспользуйтесь кнопкой ниже:',
                             reply_markup=buttons)
        return
    buttons = create_keyboard_buttons('Назад')
    if type_to_mail == 'Текст':
        await state.set_state(AdminMenu.mailing_with_text)
        await message.answer('Хорошо! Отправьте текст, который вы собираетесь отправить участницам:',
                             reply_markup=buttons)
    elif type_to_mail == 'Фото':
        await state.set_state(AdminMenu.mailing_with_photo)
        await message.answer('Хорошо! Отправьте фото, которое вы собираетесь отправить участницам (с подписью):',
                             reply_markup=buttons)
    else:
        await state.set_state(AdminMenu.mailing_with_file)
        await message.answer('Хорошо! Отправьте файл, который вы собираетесь отправить участницам (с подписью):',
                             reply_markup=buttons)


@dp.message(AdminMenu.mailing_with_photo, F.text == 'Назад')
async def back_to_start_mailing(message: Message, state: FSMContext):
    await moment_mailing(message, state)


@dp.message(AdminMenu.mailing_with_text, F.text == 'Назад')
async def back_to_start_mailing(message: Message, state: FSMContext):
    await moment_mailing(message, state)


@dp.message(AdminMenu.mailing_with_file, F.text == 'Назад')
async def back_to_start_mailing(message: Message, state: FSMContext):
    await moment_mailing(message, state)


@dp.message(AdminMenu.mailing_with_photo, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    caption = message.caption
    await state.update_data(mailing_type='Фото', photo_id=photo_id, caption=caption)
    buttons = create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите разослать такое фото с такой подписью?', reply_markup=buttons)
    await message.answer_photo(photo=photo_id, caption=caption)


@dp.message(AdminMenu.mailing_with_file, F.document)
async def handle_photo(message: Message, state: FSMContext):
    file_id = message.document.file_id
    caption = message.caption
    await state.update_data(mailing_type='Файл', file_id=file_id, caption=caption)
    buttons = create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите разослать такой файл с такой подписью?', reply_markup=buttons)
    await message.answer_document(document=file_id, caption=caption)


@dp.message(AdminMenu.mailing_with_text, F.text == 'Подтвердить')
async def handle_text(message: Message, state: FSMContext):
    await mail_promouters(state)
    await main_bot_menu(message, state)


@dp.message(AdminMenu.mailing_with_text)
async def handle_text(message: Message, state: FSMContext):
    ans = message.text
    await state.update_data(mailing_type='Текст', text_to_mail=ans)
    buttons = create_keyboard_buttons('Подтвердить', 'Назад')
    await message.answer('Вы хотите разослать такой текст?', reply_markup=buttons)
    await message.answer(ans)


@dp.message(AdminMenu.mailing_with_file, F.text == 'Подтвердить')
async def start_file_mailing(message: Message, state: FSMContext):
    await mail_promouters(state)
    await main_bot_menu(message, state)


@dp.message(AdminMenu.mailing_with_photo, F.text == 'Подтвердить')
async def start_photo_mailing(message: Message, state: FSMContext):
    await mail_promouters(state)
    await main_bot_menu(message, state)


async def mail_promouters(state: FSMContext):
    ids = await girlsclub_db.get_all_members()
    data = await state.get_data()
    mailing_type = data['mailing_type']
    if mailing_type == 'Текст':
        content = data['text_to_mail']
    elif mailing_type == 'Фото':
        content = [data['photo_id'], data['caption']]
    else:
        content = [data['file_id'], data['caption']]
    for i in ids['data']:
        user_id = i['telegram_id']
        try:
            if mailing_type == 'Текст':
                await bot.send_message(chat_id=user_id, text=content)
            elif mailing_type == 'Фото':
                photo_id, caption = content
                await bot.send_photo(chat_id=user_id, photo=photo_id, caption=caption)
            elif mailing_type == 'Файл':
                file_id, caption = content
                await bot.send_document(chat_id=user_id, document=file_id, caption=caption)
        except:
            await bot.send_message(chat_id=config.ADMIN_ID, text=f'Не получилось отправить пользователю {user_id} '
                                                                 f'({i["full_name"]})')