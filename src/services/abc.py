from abc import ABC, abstractmethod
from uuid import UUID
from models.users import UserSettings


class QueueABC(ABC):
    def push(self, element):
        ...


class NotificationServiceABC(ABC):
    queue: QueueABC

    def send_message():
        ...
