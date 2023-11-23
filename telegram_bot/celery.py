from celery import Celery
from celery.schedules import crontab

app = Celery('telegram_bot', broker='amqp://guest:guest@rabbitmq:5672//')

from telegram_bot import tasks


app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'send-daily-message-every-morning': {
        'task': 'telegram_bot.tasks.run_daily_mailing_sync',
        'schedule': crontab(minute='*'),
    },
}
app.autodiscover_tasks()
# crontab(hour='10', minute='0')