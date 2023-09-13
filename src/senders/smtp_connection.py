import smtplib
from typing import cast

from core.config import settings
from db.base import ConnectionManager, Connector


class SMTPConnector(Connector):
    def __init__(
        self, smtp_host: str = settings.smtp_host, smtp_port: int = settings.smtp_port
    ):
        super().__init__()
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def _ping(self):
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp:
            smtp.noop()

    def connect(self) -> smtplib.SMTP:
        if not self.connection:
            self.connection = self._connect()
        return self.connection

    def _connect(self) -> smtplib.SMTP:
        return smtplib.SMTP(self.smtp_host, self.smtp_port)


class SMTPConnectionManager(ConnectionManager):
    def __init__(self, connector: SMTPConnector):
        super().__init__(connector)

    def get_connection(self) -> smtplib.SMTP:
        return cast(smtplib.SMTP, super().get_connection())
