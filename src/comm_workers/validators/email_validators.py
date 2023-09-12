from core.config import settings
from core.loggers import LOGGER
from models.emails import EmailMessages
from sendgrid.helpers.mail import From, Mail, To
from sib_api_v3_sdk import SendSmtpEmail

from .abstract import ValidatorABC


class ValidatorEmail(ValidatorABC):
    def validate_for_send(self, msg: dict) -> EmailMessages | Exception:
        # {'type_': 'email', 'recipients': {'to_': ['sergey.koltunov.228@gmail.com', 'sergeusprecious@gmail.com'], 'from_': 'sergeusprecious@gmail.com', 'subject': 'Company Context'}, 'message': '<html><body><h3>Hello Вася</h3></body></html>'}
        reformatted_message = {"message": msg.get("message")}
        reformatted_message.update(**msg.get("recipients"))
        try:
            return EmailMessages(**reformatted_message)
        except Exception as e:
            LOGGER.error(
                "Message from broker is invalid for email channel. Msg:%s, error:%s",
                msg,
                e,
            )
            return e


class ValidatorEmailSndgrd(ValidatorEmail):
    def validate_for_sender(self, msg: dict) -> Mail | Exception:
        validated = self.validate_for_send(msg)
        if not isinstance(validated, Exception):
            try:
                messages = Mail(
                    from_email=From(validated.sender),
                    to_emails=[To(recipient) for recipient in validated.recipients],
                    subject=validated.subject,
                    html_content=validated.message,
                )
            except Exception as e:
                LOGGER.error("Failed to validate emails %s for sendgrid: %s", msg, e)
                return e
            return messages
        return validated


class ValidatorEmailBrevo(ValidatorEmail):
    def validate_for_sender(self, msg: dict) -> SendSmtpEmail | Exception:
        validated = self.validate_for_send(msg)
        if not isinstance(validated, Exception):
            try:
                messages = SendSmtpEmail(
                    sender={"email": validated.sender},
                    bcc=[{"email": recipient} for recipient in validated.recipients],
                    subject=validated.subject,
                    html_content=validated.message,
                )
            except Exception as e:
                LOGGER.error("Failed to validate emails %s for brevo: %s", msg, e)
                return e
            return messages
        return validated
