from abstract import ValidatorABC
from models.emails import EmailMessages
from sendgrid.helpers.mail import Content, From, Mail, To
from utils.loggers import LOGGER


class ValidatorEmail(ValidatorABC):
    def validate_for_send(self, msg: dict) -> EmailMessages | None:
        try:
            return EmailMessages(**msg)
        except Exception as e:
            LOGGER.error("Message from the broker is invalid. Msg: %s", e)
            return None

    def validadate_for_sender(self, msg: dict, sender_name: str) -> list[Mail] | None:
        messages = []
        validated = self.validate_for_send(msg)
        if validated:
            match sender_name:
                case "SendGridAPIClient":
                    for recipient in validated.recipients:
                        try:
                            messages.append(
                                Mail(
                                    from_email=From(validated.sender),
                                    to_emails=To(recipient),
                                    subject=validated.subject,
                                    html_content=Content(
                                        "text/html", validated.message
                                    ),
                                )
                            )
                        except Exception as e:
                            LOGGER.error("Failed to validate email for sendgrid: %s", e)
                            return None
                    return messages
        return None
