from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class OrderBase(BaseModel, Config):
    id: int


class OrderInfo(OrderBase):
    user_id = Optional[int]
    payment_id = Optional[int]
    name = Optional[str]
    phone_number = Optional[str]
    email = Optional[str]
    address = Optional[str]
    status = Optional[int]


class OrderCreate(BaseModel):
    user_id = Optional[int]
    payment_id = Optional[int]
    name = Optional[str]
    phone_number = Optional[str]
    email = Optional[str]
    address = Optional[str]
    status = Optional[int]


class OrderUpdate(OrderCreate):
    pass
