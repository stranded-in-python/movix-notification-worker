import validators.email_validators as email_val
from comm_channels.email import EmailChannel
from core.config import settings
from senders.email_senders import SenderBrevo, SenderSndgrd


class CommChannelFactory:
    @staticmethod
    def build_brevo_email_channel() -> EmailChannel:
        channel = EmailChannel(
            SenderBrevo(settings.brevo_api_key), email_val.ValidatorEmailBrevo()
        )
        return channel

    @staticmethod
    def build_sndgrd_email_channel() -> EmailChannel:
        channel = EmailChannel(
            SenderSndgrd(settings.sendgrid_api_key), email_val.ValidatorEmailSndgrd()
        )
        return channel
