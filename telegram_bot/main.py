import logging
import sys
import asyncio
import aiogram
from handlers import dp, bot


async def start_bot():
    await dp.start_polling(bot)


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())


main()
