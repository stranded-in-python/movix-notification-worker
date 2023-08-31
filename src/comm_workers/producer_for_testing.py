import json

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

# old format
# channel.basic_publish(
#     exchange=settings.RMQ_main_exchange,
#     routing_key="",
#     body=b'{"sender": "sergeusprecious@gmail.com", "recipients": ["sergey.koltunov.228@gmail.com"], "subject": "testing", "message": "<strong>i am message!</strong>"}',
# )

message = {
    "notification-id": "notification-id",
    "payload": {
        "mime-type": "mime-type",
        "message": "<strong>i am message!</strong>",
        "email": {
            "sender": "sergeusprecious@gmail.com",
            "recipients": ["sergey.koltunov.228@gmail.com"],
            "subject": "testing",
        },
        "telegram": {"recipients": ["sergey.koltunov.228@gmail.com"]},
    },
}

# message = {
#     "notification-id": "notification-id",
#     "payload": {
#         "mime-type": "mime-type",
#         "message": "<strong>i am message!</strong>",
#         "email": {
#             "sender": "sergeusprecious@gmail.com",
#             "recipients": ["example@mail.com", "zhopa"],
#             "subject": "testing",
#         },
#         "telegram": {"recipients": ["sergey.koltunov.228@gmail.com"]},
#     },
# }

channel.basic_publish(
    exchange=settings.RMQ_main_exchange,
    routing_key="",
    body=json.dumps(message).encode("utf-8"),
)


print(" [x] Sent 'Hello World!'")
connection.close()
