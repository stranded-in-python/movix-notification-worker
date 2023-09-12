from uuid import UUID

from .mixins import UserIDMixin


class ChannelSettings(UserIDMixin):
    channel: str
    email_enabled: bool


class NotificationSettings(UserIDMixin):
    notification: UUID
    email_disabled: bool
