from pydantic import BaseModel


class EmailMessages(BaseModel):
    sender: str
    recipients: list
    subject: str
    message: str
