from abc import ABC, abstractmethod
from uuid import UUID


class StorageABC(ABC):
    @abstractmethod
    async def get_item(self, item_id: UUID):
        raise NotImplementedError
