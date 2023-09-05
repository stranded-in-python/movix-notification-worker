from pydantic import BaseModel, EmailStr, Field


class EmailMessages(BaseModel):
    sender: EmailStr = Field(alias="from_")
    recipients: list[EmailStr] = Field(alias="to_")
    subject: str
    message: str
