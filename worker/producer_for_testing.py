import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="brevo")

# channel.basic_publish(exchange="", routing_key="hello", body=b'{"hello": "world"}')
# channel.basic_publish(exchange="", routing_key="hello", body=b'ahah')
channel.basic_publish(
    exchange="",
    routing_key="brevo",
    body=b'{"sender": "sergeusprecious@gmail.com", "recipients": ["sergey.koltunov.228@gmail.com"], "subject": "testing", "message": "<strong>i am message!</strong>"}',
)
print(" [x] Sent 'Hello World!'")

connection.close()
