import os

import sib_api_v3_sdk.configuration
from core.loggers import LOGGER
from sib_api_v3_sdk import ApiClient, SendSmtpEmail, TransactionalEmailsApi

from .abstract import SenderABC


class SenderBrevo(SenderABC):
    def __init__(self, api_key: str):
        print("API_KEY!!!!!!!!!!!!!!!!!! IN INIT", api_key)
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key["api-key"] = api_key
        self.api_client = TransactionalEmailsApi(ApiClient(self.configuration))

    async def send_many(self, emails: list[SendSmtpEmail]) -> None:
        for email in emails:
            await self.send_one(email)

    async def send_one(self, email: SendSmtpEmail) -> None:
        try:
            self.api_client.send_transac_email(email, async_req=True)
        except Exception as e:
            LOGGER.error(
                "Failed to send email %s with:%s",
                email,
                e,
            )
