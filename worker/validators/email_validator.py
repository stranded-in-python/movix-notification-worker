import sendgrid.helpers.mail as sndgrd_mail
from abstract import ValidatorABC
from models.emails import EmailMessages
from utils.loggers import LOGGER


class ValidatorEmail(ValidatorABC):
    def validate_for_send(self, msg: dict) -> EmailMessages | None:
        try:
            return EmailMessages(**msg)
        except Exception as e:
            LOGGER.error("Message from the broker is invalid. Msg: %s", e)
            return None

    def validadate_for_sender(
        self, msg: dict, sender_name: str
    ) -> sndgrd_mail.Mail | None:
        messages = []
        validated = self.validate_for_send(msg)
        if validated:
            match sender_name:
                case "SendGridAPIClient":
                    for recipient in validated.recipients:
                        try:
                            messages.append(
                                sndgrd_mail.Mail(
                                    from_email=sndgrd_mail.From(validated.sender),
                                    to_emails=sndgrd_mail.To(recipient),
                                    subject=validated.subject,
                                    html_content=sndgrd_mail.Content(validated.message),
                                )
                            )
                        except Exception as e:
                            LOGGER.error("Failed to validate email for sendgrid: %s", e)
                            return None
        return validated
