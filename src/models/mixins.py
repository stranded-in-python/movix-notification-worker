from uuid import UUID

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    id: UUID


class UserIDMixin(BaseModel):
    user_id: UUID
