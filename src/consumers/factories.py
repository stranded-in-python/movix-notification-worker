import validators.email_validators as email_val
from comm_channels.email import EmailChannel
from core.config import settings
from core.sender_enums import EmailSenders
from db.psql import DBTemplatePSQL
from enrichers.templates_enricher import TemplateEnricher
from senders.email_senders import SenderBrevo, SenderSndgrd
from storages.template_storages import StorageTemplate


class CommChannelFactory:
    @staticmethod
    def build_email_channel() -> EmailChannel:
        channel = EmailChannel(**getattr(EmailSenders, settings.smtp_host).value)
        return channel
