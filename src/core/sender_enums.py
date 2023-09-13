from enum import Enum

import validators.email_validators as email_val
from core.config import settings
from db.psql import DBTemplatePSQL
from enrichers.templates_enricher import TemplateEnricher
from senders.email_senders import SenderBrevo, SenderSMTP, SenderSndgrd
from senders.smtp_connection import SMTPConnectionManager
from storages.template_storages import StorageTemplate


class EmailSenders(Enum):
    BREVO = {
        "sender": SenderBrevo(settings.brevo_api_key),
        "validator": email_val.ValidatorEmailBrevo(),
        "storage": StorageTemplate(DBTemplatePSQL()),
        "enricher": TemplateEnricher(),
    }
    SENDGRID = {
        "sender": SenderSndgrd(settings.sendgrid_api_key),
        "validator": email_val.ValidatorEmailSndgrd(),
        "storage": StorageTemplate(DBTemplatePSQL()),
        "enricher": TemplateEnricher(),
    }
    MAILHOG = {
        "sender": SenderSMTP(),
        "validator": email_val.ValidatorEmailSMTP(),
        "storage": StorageTemplate(DBTemplatePSQL()),
        "enricher": TemplateEnricher(),
    }
