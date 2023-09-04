from core.config import settings
from core.loggers import LOGGER
from models.emails import EmailMessages
from sendgrid.helpers.mail import Content, From, Mail, To
from sib_api_v3_sdk import SendSmtpEmail

from .abstract import ValidatorABC


class ValidatorEmail(ValidatorABC):
    def validate_for_send(self, msg: dict) -> EmailMessages | None:
        reformatted_message = {"message": msg.get("message")}
        reformatted_message.update(**msg.get(settings.key_for_email_channel))
        try:
            return EmailMessages(**reformatted_message)
        except Exception as e:
            LOGGER.error(
                "Message from the broker is invalid for email channel. Msg:%s, error:%s",
                msg,
                e,
            )
            return None


class ValidatorEmailSndgrd(ValidatorEmail):
    def validate_for_sender(self, msg: dict) -> Mail | None:
        validated = self.validate_for_send(msg)
        if validated:
            try:
                messages = Mail(
                    from_email=From(validated.sender),
                    to_emails=[To(recipient) for recipient in validated.recipients],
                    subject=validated.subject,
                    html_content=validated.message,
                )
            except Exception as e:
                LOGGER.error("Failed to validate emails %s for brevo: %s", msg, e)
                return None
            return messages
        return None


class ValidatorEmailBrevo(ValidatorEmail):
    def validate_for_sender(self, msg: dict) -> SendSmtpEmail | None:
        validated = self.validate_for_send(msg)
        if validated:
            try:
                messages = SendSmtpEmail(
                    sender={"email": validated.sender},
                    to=[{"email": recipient} for recipient in validated.recipients],
                    subject=validated.subject,
                    html_content=validated.message,
                )
            except Exception as e:
                LOGGER.error("Failed to validate emails %s for brevo: %s", msg, e)
                return None
            return messages
        return None
