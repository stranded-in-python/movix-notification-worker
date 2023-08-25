from channels.abstract import ChannelABC
from rmqconsumer import ReconnectingConsumer
from utils.async_utils import sync
from utils.loggers import LOGGER


class AsyncWorker(ReconnectingConsumer):
    def __init__(
        self, amqp_url: str, comm_channel: ChannelABC, queue_name: str, routing_key: str
    ):
        super().__init__(amqp_url)
        self.comm_channel = comm_channel
        self.QUEUE = queue_name
        self.ROUTING_KEY = routing_key

    @sync
    async def consumer(self, _unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel _unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param bytes body: The message body

        """
        LOGGER.info(
            "Received message # %s from %s: %s",
            basic_deliver.delivery_tag,
            properties.app_id,
            body,
        )
        await self.comm_channel.handle_message(body)
