from abc import ABC, abstractmethod


class ChannelABC(ABC):
    def __init__(self, sender, parser):
        self.sender = sender
        self.parser = parser

    @abstractmethod
    async def handle_message(self, msg: bytes):
        raise NotImplementedError


class EmailChannelABC(ChannelABC):
    def __init__(self, sender, parser):
        self.sender = sender
        self.parser = parser

    @abstractmethod
    async def handle_message(self, msg: bytes):
        raise NotImplementedError

    @abstractmethod
    async def send_email(self, recipient: list, message: str):
        raise NotImplementedError

    async def send_many_emails(self, recipients: list, message: str):
        raise NotImplementedError
