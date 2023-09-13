from comm_channels.email import EmailChannel
from core.config import settings
from core.sender_enums import EmailSenders


class CommChannelFactory:
    @staticmethod
    def build_email_channel() -> EmailChannel:
        channel = EmailChannel(**getattr(EmailSenders, settings.smtp_sender).value)
        return channel
