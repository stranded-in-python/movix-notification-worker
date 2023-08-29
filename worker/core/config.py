from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    sendgrid_api_key: str = Field("NoKey", env="SNDGRD_API_KEY")
    brevo_api_key: str = Field("NoKey", env="BREVO_API_KEY")

    amqp_url: str = Field("amqp://guest:guest@localhost:5672/%2F", env="AMQP_URL")
    RMQ_prefetch_count: int = Field(2, env="RMQ_PREFETCH_COUNT")
    RMQ_main_exchange: str = Field("main", env="RMQ_MAIN_EXCHANGE")
    RMQ_dead_exchange: str = Field("dead", env="RMQ_DEAD_EXCHANGE")
    RMQ_main_queue: str = Field("main", env="RMQ_MAIN_QUEUE")
    RMQ_dead_queue: str = Field("dead", env="RMQ_DEAD_QUEUE")
    RMQ_dead_ttl: int = Field(60 * 1000, env="RMQ_DEAD_TTL")
    RMQ_retry_count: int = Field(2, env="RMQ_RETRY_COUNT")

    key_for_email_channel: str = Field("email")


settings = Settings()
