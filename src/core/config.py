import os
from uuid import UUID

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    project_name: str = "movix-notifications"

    base_dir = os.path.dirname(os.path.dirname(__file__))


class PublisherProperties(BaseSettings):
    amqp_url: str = (
        "amqp://guest:guest@localhost:5672/"
        "%2F?connection_attempts=3&heartbeat=3600"  # flake8: noqa
    )
    exchange: str = "movix-notification"
    exchange_type: str = "fanout"
    publish_interval: int = 1
    queue: str = "movix-notification"
    routing_key: str = "notification.email"

    auth_user_rights_endpoint: str = 'http://auth:8000/api/v1/users/user_id/roles'
    access_token_secret: SecretStr = SecretStr('ACCESS')
    access_token_audience: str = 'movix:auth'

class EventsProperties(BaseSettings):
    on_registration_id: UUID = ""
    on_registration_vars: list[str] = [""]
    on_registration_send_from: str = "welcom@movix.ru"
    on_registration_subject: str = "Confirm you email"


settings = Settings()
publisher_properties = PublisherProperties()
events_properties = EventsProperties()
