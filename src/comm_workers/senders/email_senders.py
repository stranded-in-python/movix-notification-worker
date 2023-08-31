import sib_api_v3_sdk.configuration
from core.loggers import LOGGER
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sib_api_v3_sdk import ApiClient, SendSmtpEmail, TransactionalEmailsApi
from sib_api_v3_sdk.rest import ApiException

from .abstract import SenderABC


class SenderBrevo(SenderABC):
    def __init__(self, api_key: str):
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key["api-key"] = api_key
        self.api_client = TransactionalEmailsApi(ApiClient(self.configuration))

    async def send(self, email: SendSmtpEmail) -> None:
        try:
            return self.api_client.send_transac_email(email, async_req=True).get()
        except Exception as e:
            LOGGER.error(
                "Failed to send email %s with:%s",
                email,
                e,
            )
            return e


class SenderSndgrd(SenderABC, SendGridAPIClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)

    async def send(self, email: Mail) -> None:
        """
        send_mail wraps Twilio SendGrid's API client, and makes a POST request to
        the api/v3/mail/send endpoint with `email`.
        Args:
            email<sendgrid.helpers.mail.Mail>: single mail object.
        """
        try:
            self.send(email)
        except ApiException as e:
            LOGGER.error(
                "Failed to send email %s with:%s",
                email,
                e.reason,
            )
            return e.reason
