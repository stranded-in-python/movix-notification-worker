from uuid import UUID

from db.abstract import DBTemplateABC

from .abstract import StorageABC


class StorageTemplate(StorageABC):
    def __init__(self, db: DBTemplateABC):
        self.db = db

    async def get_item(self, item_id: UUID) -> str:
        return await self.db.get_one_template(item_id)
