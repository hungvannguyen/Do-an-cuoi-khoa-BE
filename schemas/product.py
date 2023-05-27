from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class ProductBase(BaseModel, Config):
    id: Optional[int]


class ProductInfo(ProductBase):
    name: Optional[str]
    quantity: Optional[str]
    img_url: Optional[str]
    description: Optional[str]


class ProductCreate(BaseModel):
    cat_id: int
    name: Optional[str]
    quantity: Optional[int]
    img_url: Optional[str]
    status: Optional[int]
    description: Optional[str]


class ProductUpdate(ProductCreate):
    pass
