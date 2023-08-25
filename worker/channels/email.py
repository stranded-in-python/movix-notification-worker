import json

from abstract import EmailChannelABC
from senders.abstract import SenderABC
from validators.abstract import ValidatorABC


class EmailChannel(EmailChannelABC):
    def __init__(self, sender: SenderABC, validator: ValidatorABC):
        self.sender = sender
        self.validator = validator

    async def handle_message(self, msg: bytes):
        validated_messages = self.validator.validate_for_sender(
            json.loads(msg), type(self.validator).__name__
        )
        if validated_messages:
            await self.sender(validated_messages)
