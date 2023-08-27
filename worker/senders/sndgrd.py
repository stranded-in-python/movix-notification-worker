import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from utils.loggers import LOGGER


class SenderSndgrd(SendGridAPIClient):
    def __init__(self, api_key: str):
        super().__init__(os.environ.get("SENDGRID_API_KEY"))

    async def send_many(self, emails: list[Mail]) -> None:
        """
        send_many creates a number of non-blocking tasks (to send email)
        that will run on the existing event loop. Due to non-blocking nature,
        you can include a callback that will run after all tasks have been queued.

        Args:
            emails<list>: contains any # of `sendgrid.helpers.mail.Mail`.
        """
        for email in emails:
            await self.send_one(email)

    async def send_one(self, email: Mail) -> None:
        """
        send_mail wraps Twilio SendGrid's API client, and makes a POST request to
        the api/v3/mail/send endpoint with `email`.
        Args:
            email<sendgrid.helpers.mail.Mail>: single mail object.
        """
        try:
            self.send(email)
        except Exception as e:
            LOGGER.error(
                "Failed to send email %s with:%s",
                email,
                e,
            )
