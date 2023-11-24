from telegram_bot.loader import dp, bot
from telegram_bot.service import girlsclub_db


from telegram_bot.assets.configs import config


async def daily_mailing():
    members = await girlsclub_db.get_all_members()

    # await bot.send_message(chat_id=config.ADMIN_ID, text=f'{members}')

    for i in members['data']:
        t_id = i['telegram_id']
        try:
            await bot.send_message(chat_id=t_id, text=f'Это ежеминутная рассылка! Всем привет! :3')
        except:
            await bot.send_message(chat_id=config.ADMIN_ID,
                                   text=f'Не получилось отправить сообщение участнице {i["full_name"]}\n'
                                        f'Ее уникальный номер: {i["unique_id"]}')