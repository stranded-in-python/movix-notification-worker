import asyncio
import logging

from consumers.messagequeue import IncommingMessageQueue
from core.config import settings

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

mq = IncommingMessageQueue(settings.amqp_url, "brevo")

print(mq._amqp_url)

if __name__ == "__main__":

    mq.start_running()
