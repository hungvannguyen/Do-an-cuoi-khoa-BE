from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class PaymentBase(BaseModel, Config):
    id: int


class PaymentCreate(BaseModel):
    payment_type_id: Optional[int]
    status: Optional[int]


class PaymentUpdate(PaymentCreate):
    pass
