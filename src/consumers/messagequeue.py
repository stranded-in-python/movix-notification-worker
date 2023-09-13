import asyncio
import json

import aio_pika

from comm_channels.abstract import ChannelABC
from core.config import settings
from core.loggers import LOGGER


class IncommingMessageQueue:
    def __init__(self, comm_channels: dict[str, ChannelABC]):
        self._amqp_url = settings.amqp_url

        self._connection = None
        self._channel = None
        self._main_exchange = None
        self._dead_exchange = None
        self._main_queue = None
        self._dead_queue = None

        self.comm_channels = comm_channels

    async def connect(
        self, loop: asyncio.BaseEventLoop
    ) -> aio_pika.abc.AbstractRobustConnection:
        LOGGER.info("Connecting to %s", self._amqp_url)
        return await aio_pika.connect_robust(self._amqp_url, loop=loop)

    async def open_channel(self) -> aio_pika.channel.Channel:
        LOGGER.info("Opening channel")
        channel = await self._connection.channel()
        await channel.set_qos(prefetch_count=settings.RMQ_prefetch_count)
        return channel

    async def declare_exchanges(self):
        LOGGER.info(
            "Declaring Exchanges %s, %s",
            settings.RMQ_main_exchange,
            settings.RMQ_dead_exchange,
        )
        main_exchange = await self._channel.declare_exchange(
            settings.RMQ_main_exchange, type="fanout", durable=True
        )
        dead_exchange = await self._channel.declare_exchange(
            settings.RMQ_dead_exchange, type="fanout", durable=True
        )
        return main_exchange, dead_exchange

    async def declare_queues(self) -> aio_pika.Queue:
        LOGGER.info(
            "Declaring queues %s, %s", settings.RMQ_main_queue, settings.RMQ_dead_queue
        )
        main_arguments = {
            # при nack-е будут попадать в dead_letter_exchange
            "x-dead-letter-exchange": settings.RMQ_dead_exchange
        }
        dead_arguments = {
            # при nack-е будут попадать в dead_letter_exchange
            "x-message-ttl": settings.RMQ_dead_ttl,
            # также не забываем, что у очереди "мертвых" сообщений
            # должен быть свой dead letter exchange
            "x-dead-letter-exchange": settings.RMQ_main_exchange,
        }
        main_queue = await self._channel.declare_queue(
            name=settings.RMQ_main_queue, durable=True, arguments=main_arguments
        )
        dead_queue = await self._channel.declare_queue(
            name=settings.RMQ_dead_queue, durable=True, arguments=dead_arguments
        )
        await main_queue.bind(self._main_exchange)
        await dead_queue.bind(self._dead_exchange)
        return main_queue, dead_queue

    def can_retry(self, headers):
        """
        Заголовок x-death проставляется при прохождении сообщения через dead letter exchange.
        С его помощью можно понять, какой "круг" совершает сообщение.
        """
        deaths = (headers or {}).get("x-death")
        if not deaths:
            return True
        if deaths[0]["count"] >= settings.RMQ_retry_count:
            return False
        return True

    async def process_message(
        self, message: aio_pika.abc.AbstractIncomingMessage
    ) -> None:
        async with message.process(ignore_processed=True):
            LOGGER.info("Received message %s", message.body)
            if self.can_retry(message.headers):
                LOGGER.info("Message doesn't smell")
                message_dict = json.loads(message.body.decode("utf-8"))
                try:
                    needed_channel = self.comm_channels[message_dict.get("type_")]
                except KeyError:
                    LOGGER.error("There's no comm channel for type %s", needed_channel)
                result = await needed_channel.handle_message(message_dict)
                if isinstance(result, Exception):
                    await message.reject(requeue=False)
                    LOGGER.warning("Message rejected!")
                return None
            LOGGER.warning(
                "Message %s smells and acquired to clean queue!", message.body
            )
            await message.ack()

    async def start_consuming(self, loop: asyncio.BaseEventLoop):
        self._connection = await self.connect(loop)
        self._channel = await self.open_channel()

        self._main_exchange, self._dead_exchange = await self.declare_exchanges()
        self._main_queue, self._dead_queue = await self.declare_queues()

        await self._main_queue.consume(self.process_message)

        print(self.comm_channels)

        await asyncio.Future()

    async def stop(self):
        LOGGER.info("Closing connection")
        await self._connection.close()

    # entry point
    def start_running(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.start_consuming(loop))
        except KeyboardInterrupt:
            loop.run_until_complete(self.stop())
