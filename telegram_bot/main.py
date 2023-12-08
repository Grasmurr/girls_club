import logging, sys, json, asyncio, aiogram
from handlers import dp, bot
from telegram_bot.service.daily_mailing import daily_mailing

import aio_pika


async def on_rabbitmq_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        if data['command'] == 'start_daily_mailing':
            await daily_mailing()


async def rabbitmq_listener(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/", loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue("mailing_queue")
    await queue.consume(on_rabbitmq_message)


async def main():
    # Установка логирования
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    loop = asyncio.get_event_loop()
    loop.create_task(rabbitmq_listener(loop))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
