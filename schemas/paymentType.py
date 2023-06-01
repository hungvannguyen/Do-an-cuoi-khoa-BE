from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class PaymentTypeBase(BaseModel, Config):
    id: int


class PaymentTypeCreate(BaseModel):
    name: Optional[str]


class PaymentTypeUpdate(PaymentTypeCreate):
    pass
