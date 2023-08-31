from pydantic import BaseModel, Field


class EmailMessages(BaseModel):
    sender: str
    recipients: list = Field(alias="to")
    subject: str
    message: str
