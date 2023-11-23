from celery import shared_task
import pika, json

@shared_task
def send_mailing_signal():
    connection_params = pika.ConnectionParameters(host='rabbitmq')
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    message = json.dumps({"command": "start_daily_mailing"})
    channel.basic_publish(exchange='', routing_key='mailing_queue', body=message)
    connection.close()


