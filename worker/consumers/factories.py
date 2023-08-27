import os

from channels.email import EmailChannel
from senders.sndgrd import SenderSndgrd
from validators.email_validator import ValidatorEmail

from .rmqconsumer import ReconnectingConsumer
from .workers import AsyncConsumer


class WorkerFactory:
    @staticmethod
    def build_sndrgd_worker(amqp_url: str, queue_name: str, routing_key: str):
        channel = EmailChannel(
            SenderSndgrd(os.environ.get("SENDGRID_API_KEY")), ValidatorEmail()
        )
        consumer = AsyncConsumer(amqp_url, channel, queue_name, routing_key)
        worker = ReconnectingConsumer(amqp_url, consumer)
        return worker
