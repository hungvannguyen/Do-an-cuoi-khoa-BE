from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class MailConfirm(BaseModel, Config):
    mail_to: str

