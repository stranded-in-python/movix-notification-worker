from abc import ABC, abstractmethod
from uuid import UUID


class DBTemplateABC(ABC):
    @abstractmethod
    async def get_one_template(template_id: UUID):
        raise NotImplementedError
