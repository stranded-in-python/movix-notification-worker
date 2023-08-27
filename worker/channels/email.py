import json

from senders.abstract import SenderABC
from utils.loggers import LOGGER
from validators.abstract import ValidatorABC

from .abstract import ChannelABC


class EmailChannel(ChannelABC):
    def __init__(self, sender: SenderABC, validator: ValidatorABC):
        self.sender = sender
        self.validator = validator

    async def handle_message(self, msg: bytes):
        try:
            validated_messages = self.validator.validate_for_sender(
                json.loads(msg), type(self.sender).__name__
            )
        except Exception as e:
            LOGGER.error("Could not handle the message %s with exception: %s", msg, e)
            return e
        if validated_messages:
            await self.sender.send_many(validated_messages)
