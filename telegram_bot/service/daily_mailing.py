from telegram_bot.loader import dp, bot
from telegram_bot.service import girlsclub_db


from telegram_bot.assets.configs import config


async def daily_mailing():
    members = await girlsclub_db.get_all_members()
    await bot.send_message(chat_id=config.ADMIN_ID, text=f'{members}')