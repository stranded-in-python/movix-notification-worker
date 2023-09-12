from uuid import UUID

from .abc import NotificationSettingsChannelDBABC, NotificationSettingsDBABC

class NotificationSettingsChannelDB(NotificationSettingsChannelDBABC):
    def __init__(self):
        pass

    async def create(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError

    async def get(self, user_id: UUID):
        raise NotImplementedError
    
    async def change(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError
    
    async def delete(self, channel: str, user_id: UUID):
        raise NotImplementedError
    

class NotificationSettingsDB(NotificationSettingsDBABC):
    def __init__(self):
        pass

    async def create(self, notification_id: UUID, disabled: bool, user_id: UUID):
        raise NotImplementedError

    async def get(self, user_id: UUID):
        raise NotImplementedError
    
    async def change(self, notification_id: UUID, disabled: bool, user_id: UUID):
        raise NotImplementedError
    
    async def delete(self, notification_id: UUID, user_id: UUID):
        raise NotImplementedError
