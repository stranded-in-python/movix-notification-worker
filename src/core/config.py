from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    logger_level: str = Field("INFO", env="LOGGER_LEVEL")

    sendgrid_api_key: str = Field("", env="SNDGRD_API_KEY")
    brevo_api_key: str = Field("", env="BREVO_API_KEY")

    smtp_host: str = Field("BREVO", env="SMTP_HOST")

    amqp_login: str = Field("guest", env="AMQP_LOGIN")
    amqp_password: str = Field("guest", env="AMQP_PASSWORD")
    amqp_host: str = Field("localhost", env="AMQP_HOST")
    amqp_port: str = Field("5672", env="AMQP_PORT")
    RMQ_prefetch_count: int = Field(2, env="RMQ_PREFETCH_COUNT")
    RMQ_main_exchange: str = Field("main", env="RMQ_MAIN_EXCHANGE")
    RMQ_dead_exchange: str = Field("dead", env="RMQ_DEAD_EXCHANGE")
    RMQ_main_queue: str = Field("main", env="RMQ_MAIN_QUEUE")
    RMQ_dead_queue: str = Field("dead", env="RMQ_DEAD_QUEUE")
    RMQ_input_dead_ttl: int = Field(60, env="RMQ_DEAD_TTL")
    RMQ_retry_count: int = Field(2, env="RMQ_RETRY_COUNT")

    psql_db_name: str = Field("yamp_movies_db", env="POSTGRES_DB")
    psql_user: str = Field("yamp_dummy", env="POSTGRES_USER")
    psql_password: str = Field("qweasd123", env="POSTGRES_PASSWORD")
    psql_host: str = Field("localhost", env="POSTGRES_HOST")
    psql_port: int = Field(5432, env="POSTGRES_PORT")

    wait_up_to: int = Field(60 * 60 * 12)
    waiting_interval: int = Field(60 * 30)
    waiting_factor: int = Field(2)
    first_nap: float = Field(0.1)

    templates_collection: str = Field(
        "notification.template", env="TEMPLATES_COLLECTION"
    )
    templates_id_field: str = Field("id", env="TEMPLATES_ID_FIELD")
    templates_body_field: str = Field("body", env="TEMPLATES_BODY_FIELD")

    @property
    def amqp_url(self):
        return f"amqp://{self.amqp_login}:{self.amqp_password}@{self.amqp_host}:{self.amqp_port}/%2F"

    @property
    def RMQ_dead_ttl(self):
        return self.RMQ_input_dead_ttl * 1000


settings = Settings()
