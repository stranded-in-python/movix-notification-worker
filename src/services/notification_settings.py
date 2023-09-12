from uuid import UUID

from .abc import (NotificationChannelSettingsServiceABC,
                  NotificationSettingsServiceABC)


class NotificationChannelSettingsService(NotificationChannelSettingsServiceABC):
    def __init__(self):
        pass

    async def create_channel_setting(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError

    async def get_channel_settings(self, user_id: UUID):
        raise NotImplementedError

    async def change_channel_settings(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError

    async def delete_channel_settings(self, channel: str, user_id: UUID):
        raise NotImplementedError


class NotificationSettingsServiceABC(NotificationSettingsServiceABC):
    def __init__(self):
        pass

    async def create_notification_setting(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ):
        raise NotImplementedError

    async def get_notification_settings(self, user_id: UUID):
        raise NotImplementedError

    async def change_notification_settings(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ):
        raise NotImplementedError

    async def delete_notification_settings(self, notification_id: UUID, user_id: UUID):
        raise NotImplementedError
