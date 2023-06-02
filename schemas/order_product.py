from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class OrderProductBase(BaseModel):
    id: int


class OrderProductCreate(BaseModel):
    order_id: Optional[int]
    product_id: Optional[int]
    quantity: Optional[int]
    price: Optional[float]


class OrderProductUpdate(OrderProductCreate):
    pass
