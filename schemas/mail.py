from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class MailCreate(BaseModel, Config):
    mail_to: str
    title: str
    content: str
    img: Optional[str]
    file: Optional[str]