from enum import Enum

import validators.email_validators as email_val
from core.config import settings
from senders.email_senders import SenderBrevo, SenderSndgrd
from db.psql import DBTemplatePSQL
from enrichers.templates_enricher import TemplateEnricher
from storages.template_storages import StorageTemplate


class EmailSenders(Enum):
    BREVO = {"sender": SenderBrevo(settings.brevo_api_key), "validator": email_val.ValidatorEmailBrevo(), "storage":StorageTemplate(DBTemplatePSQL()), "enricher":TemplateEnricher()}
    SENDGRID = {"sender": SenderSndgrd(settings.sendgrid_api_key), "validator": email_val.ValidatorEmailSndgrd(), "storage": StorageTemplate(DBTemplatePSQL()), "enricher": TemplateEnricher()}
    MAILHOG = None
