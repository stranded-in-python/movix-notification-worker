from abc import ABC, abstractmethod
from uuid import UUID

class QueueABC(ABC):
    def push(self, element):
        ...


class NotificationServiceABC(ABC):
    queue: QueueABC

    def send_message():
        ...

class NotificationSettingsServiceABC(ABC):
    @abstractmethod
    async def change_channel_sending(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError
    
    @abstractmethod
    async def change_notification_sending(self, notification_id: UUID, disabled: bool, user_id: UUID):
        raise NotImplementedError
