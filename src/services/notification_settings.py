from uuid import UUID

from .abc import NotificationSettingsServiceABC

class NotificationSettingsService(NotificationSettingsServiceABC):
    def __init__(self):
        pass

    async def change_channel_sending(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError
    
    async def change_notification_sending(self, notification_id: UUID, disabled: bool, user_id: UUID):
        raise NotImplementedError
