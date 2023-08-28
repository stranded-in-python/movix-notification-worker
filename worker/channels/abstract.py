from abc import ABC, abstractmethod


class ChannelABC(ABC):
    def __init__(self, sender, parser):
        self.sender = sender
        self.parser = parser

    @abstractmethod
    async def handle_message(self, msg: bytes) -> None:
        raise NotImplementedError
