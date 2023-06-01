from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class CartBase(BaseModel, Config):
    id: int


class CartInfo(CartBase):
    prd_id: Optional[int]
    quantity: Optional[int]


class CartCreate(BaseModel):
    prd_id: Optional[int]
    quantity: Optional[int]


class CartUpdate(CartCreate):
    pass