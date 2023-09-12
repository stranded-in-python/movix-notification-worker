from abc import ABC, abstractmethod
from uuid import UUID


class DBTemplateABC(ABC):
    @abstractmethod
    async def get_one_template(self, template_id: UUID) -> str:
        raise NotImplementedError
