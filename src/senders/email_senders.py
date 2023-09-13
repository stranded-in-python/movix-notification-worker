from email.mime.multipart import MIMEMultipart

import sib_api_v3_sdk.configuration
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sib_api_v3_sdk import ApiClient, SendSmtpEmail, TransactionalEmailsApi
from sib_api_v3_sdk.rest import ApiException

from core.loggers import LOGGER

from .abstract import SenderABC
from .smtp_connection import SMTPConnectionManager, SMTPConnector


class SenderBrevo(SenderABC):
    def __init__(self, api_key: str):
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key["api-key"] = api_key
        self.api_client = TransactionalEmailsApi(ApiClient(self.configuration))

    async def send(self, email: SendSmtpEmail) -> None | Exception:
        try:
            result = self.api_client.send_transac_email(email, async_req=True)
            result.get()
        except Exception as e:
            LOGGER.error("Failed to send email %s with:%s", email, e)
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
            await self.send(email)
        except ApiException as e:
            LOGGER.error("Failed to send email %s with:%s", email, e.reason)
            return e.reason


class SenderSMTP(SenderABC):
    def __init__(
        self, manager: SMTPConnectionManager = SMTPConnectionManager(SMTPConnector())
    ):
        self.manager = manager

    async def send(self, email: MIMEMultipart):
        # result = self.manager.get_connection().sendmail(email["From"], to_addrs=email["Bcc"], msg=email.as_string())
        try:
            self.manager.get_connection().send_message(email)
        except Exception as e:
            LOGGER.error("Failed to send email %s with:%s", email, e)
            return e
