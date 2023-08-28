import validators.email_validators as email_val
from channels.email import EmailChannel
from core.config import settings
from senders.brevo import SenderBrevo
from senders.sndgrd import SenderSndgrd

from .rmqconsumer import ReconnectingConsumer
from .workers import AsyncConsumer


class WorkerFactory:
    @staticmethod
    def build_sndgrd_worker(
        queue_name: str,
        routing_key: str,
        amqp_url: str = settings.amqp_url,
    ):
        channel = EmailChannel(
            SenderSndgrd(settings.sendgrid_api_key), email_val.ValidatorEmailSndgrd()
        )
        consumer = AsyncConsumer(amqp_url, channel, queue_name, routing_key)
        worker = ReconnectingConsumer(amqp_url, consumer)
        return worker

    @staticmethod
    def build_brevo_worker(
        queue_name: str,
        routing_key: str,
        amqp_url: str = settings.amqp_url,
    ):
        channel = EmailChannel(
            SenderBrevo(settings.brevo_api_key), email_val.ValidatorEmailBrevo()
        )
        consumer = AsyncConsumer(amqp_url, channel, queue_name, routing_key)
        worker = ReconnectingConsumer(amqp_url, consumer)
        return worker
