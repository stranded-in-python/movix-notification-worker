import asyncio

import aio_pika
from core.config import settings
from core.loggers import LOGGER


class IncommingMessageQueue:
    def __init__(self, amqp_url: str, queue_name: str):
        self._amqp_url = amqp_url
        self._queue_name = queue_name
        self._prefetch_count = settings.consume_prefetch_count

        self._connection = None
        self._channel = None
        self._queue = None

    async def connect(
        self, loop: asyncio.BaseEventLoop
    ) -> aio_pika.connection.Connection:
        LOGGER.info("Connecting to %s", self._amqp_url)
        return await aio_pika.connect_robust(self._amqp_url, loop=loop)

    async def open_channel(self) -> aio_pika.channel.Channel:
        LOGGER.info("Opening channel")
        channel = await self._connection.channel()
        await channel.set_qos(prefetch_count=self._prefetch_count)
        return channel

    async def declare_queue(self) -> aio_pika.Queue:
        LOGGER.info("Declaring queue %s", self._queue_name)
        return await self._channel.declare_queue(name=self._queue_name)

    async def process_message(
        self, message: aio_pika.abc.AbstractIncomingMessage
    ) -> None:
        async with message.process():
            LOGGER.info("Received message %s", message.body)

    async def start_consuming(self, loop: asyncio.BaseEventLoop):
        self._connection = await self.connect(loop)
        self._channel = await self.open_channel()
        self._queue = await self.declare_queue()

        await self._queue.consume(self.process_message)

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
