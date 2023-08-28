from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    sendgrid_api_key: str = Field("NoKey", env="SNDGRD_API_KEY")
    brevo_api_key: str = Field("NoKey", env="BREVO_API_KEY")

    amqp_url: str = Field("amqp://guest:guest@localhost:5672/%2F", env="AMQP_URL")


settings = Settings()
