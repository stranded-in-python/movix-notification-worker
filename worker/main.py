import asyncio
import logging

from consumers.factories import CommChannelFactory
from consumers.messagequeue import IncommingMessageQueue

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)

LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


if __name__ == "__main__":
    factory = CommChannelFactory()
    needed_comm_channels = [
        factory.build_brevo_email_channel()
    ]  # сюда добавляются и другие если есть
    mq = IncommingMessageQueue(needed_comm_channels)
    mq.start_running()
