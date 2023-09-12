from abc import ABC, abstractmethod
from uuid import UUID
from db.notifications import BaseNotificationDatabase
from models.users import UserChannels


class QueueABC(ABC):
    def push(self, element):
        ...


class UserServiceABC(ABC, UserChannels):
    async def get_users_channels() -> list[UserChannels]:
        ...


class NotificationServiceABC(ABC):
    queue: QueueABC
    notification_db: BaseNotificationDatabase
    user_service: UserServiceABC

    def send_message():
        ...

class NotificationSettingsServiceABC(ABC):
    @abstractmethod
    async def change_channel_sending(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError
    
    @abstractmethod
    async def change_notification_sending(self, notification_id: UUID, disabled: bool, user_id: UUID):
        raise NotImplementedError
