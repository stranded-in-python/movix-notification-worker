from abc import ABC, abstractmethod
from collections.abc import Iterable


class SenderABC(ABC):
    @abstractmethod
    async def send_many(self, messages: Iterable) -> None:
        raise NotImplementedError

    @abstractmethod
    async def send_one(self, message) -> None:
        raise NotImplementedError
