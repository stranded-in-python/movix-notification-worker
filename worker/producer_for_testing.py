import pika
from core.config import settings

main_arguments = {
    # при nack-е будут попадать в dead_letter_exchange
    "x-dead-letter-exchange": settings.RMQ_dead_exchange,
}
dead_arguments = {
    # при nack-е будут попадать в dead_letter_exchange
    "x-message-ttl": settings.RMQ_dead_ttl,
    # также не забываем, что у очереди "мертвых" сообщений
    # должен быть свой dead letter exchange
    "x-dead-letter-exchange": settings.RMQ_main_exchange,
}

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()


channel.exchange_declare(
    settings.RMQ_main_exchange, exchange_type="fanout", durable=True
)
channel.exchange_declare(
    settings.RMQ_dead_exchange, exchange_type="fanout", durable=True
)


channel.queue_declare(
    queue=settings.RMQ_main_queue, durable=True, arguments=main_arguments
)
channel.queue_declare(
    queue=settings.RMQ_dead_queue, durable=True, arguments=dead_arguments
)

channel.queue_bind(settings.RMQ_dead_queue, settings.RMQ_dead_exchange)

# связываем основную очередь с входным exchange
channel.queue_bind(settings.RMQ_dead_queue, settings.RMQ_dead_exchange)

# channel.basic_publish(exchange="", routing_key="hello", body=b'{"hello": "world"}')
# channel.basic_publish(exchange="", routing_key="hello", body=b'ahah')


channel.basic_publish(
    exchange=settings.RMQ_main_exchange,
    routing_key="",
    body=b'{"sender": "sergeusprecious@gmail.com", "recipients": ["sergey.koltunov.228@gmail.com"], "subject": "testing", "message": "<strong>i am message!</strong>"}',
)
print(" [x] Sent 'Hello World!'")

# while True:
#     try:
#         pass
#     except KeyboardInterrupt:
#         connection.close()

connection.close()
