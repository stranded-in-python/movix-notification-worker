from abc import ABC


class QueueABC(ABC):
    def push(self, element):
        ...


class NotificationServiceABC(ABC):
    queue: QueueABC

    def send_message():
        ...