from core.loggers import LOGGER
from models.emails import EmailMessages
from sendgrid.helpers.mail import Content, From, Mail, To
from sib_api_v3_sdk import SendSmtpEmail

from .abstract import ValidatorABC


class ValidatorEmail(ValidatorABC):
    def validate_for_send(self, msg: dict) -> EmailMessages | None:
        try:
            return EmailMessages(**msg)
        except Exception as e:
            LOGGER.error("Message from the broker is invalid. Msg: %s", e)
            return None


class ValidatorEmailSndgrd(ValidatorEmail):
    def validate_for_sender(self, msg: dict) -> list[Mail] | None:
        messages = []
        validated = self.validate_for_send(msg)
        if validated:
            for recipient in validated.recipients:
                try:
                    messages.append(
                        Mail(
                            from_email=From(validated.sender),
                            to_emails=To(recipient),
                            subject=validated.subject,
                            html_content=Content("text/html", validated.message),
                        )
                    )
                except Exception as e:
                    LOGGER.error("Failed to validate email for sendgrid: %s", e)
                    continue
            return messages
        return None


class ValidatorEmailBrevo(ValidatorEmail):
    def validate_for_sender(self, msg: dict) -> list[SendSmtpEmail] | None:
        messages = []
        validated = self.validate_for_send(msg)
        if validated:
            for recipient in validated.recipients:
                try:
                    message = SendSmtpEmail(
                        sender={"email": validated.sender},
                        to=[{"email": recipient}],
                        subject=validated.subject,
                        html_content=validated.message,
                        headers={"Some-Custom-Name": "unique-id-1234"},
                    )
                    messages.append(message)
                except Exception as e:
                    LOGGER.error(
                        "Failed to validate email %s for brevo: %s", message, e
                    )
                    continue
            return messages
        return None
