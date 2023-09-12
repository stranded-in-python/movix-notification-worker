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


class NotificationChannelSettingsServiceABC(ABC):
    @abstractmethod
    async def create_channel_setting(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get_channel_settings(self, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def change_channel_settings(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def delete_channel_settings(self, channel: str, user_id: UUID):
        raise NotImplementedError


class NotificationSettingsServiceABC(ABC):
    @abstractmethod
    async def create_notification_setting(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ):
        raise NotImplementedError

    @abstractmethod
    async def get_notification_settings(self, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def change_notification_settings(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete_notification_settings(self, notification_id: UUID, user_id: UUID):
        raise NotImplementedError
