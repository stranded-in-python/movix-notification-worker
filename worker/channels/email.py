import json

from core.loggers import LOGGER
from senders.abstract import SenderABC
from validators.abstract import ValidatorABC

from .abstract import ChannelABC


class EmailChannel(ChannelABC):
    def __init__(self, sender: SenderABC, validator: ValidatorABC):
        self.sender = sender
        self.validator = validator

    async def handle_message(self, msg: bytes) -> None | Exception:
        try:
            validated_messages = self.validator.validate_for_sender(json.loads(msg))
        except Exception as e:
            LOGGER.error("Could not handle the message %s with exception: %s", msg, e)
            return e
        if validated_messages:
            await self.sender.send_many(validated_messages)
