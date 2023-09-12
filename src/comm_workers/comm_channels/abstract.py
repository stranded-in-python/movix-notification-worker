from abc import ABC, abstractmethod

from enrichers.abstract import TemplateEnricherABC
from senders.abstract import SenderABC
from storages.abstract import StorageABC
from validators.abstract import ValidatorABC


class ChannelABC(ABC):
    def __init__(
        self,
        sender: SenderABC,
        validator: ValidatorABC,
        storage: StorageABC,
        enricher: TemplateEnricherABC,
    ):
        self.sender = sender
        self.validator = validator
        self.storage = storage
        self.enricher = enricher

    @abstractmethod
    async def handle_message(self, msg: bytes) -> None:
        raise NotImplementedError
