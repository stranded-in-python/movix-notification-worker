from abc import ABC, abstractmethod


class SenderABC(ABC):
    @abstractmethod
    async def send(self, message: object) -> None:
        raise NotImplementedError
