from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class WarehouseBase(BaseModel, Config):
    id: int


class WarehouseCreate(BaseModel):

    city: Optional[int]
    district: Optional[int]
    ward: Optional[int]
    detail: Optional[str]


class WarehouseUpdate(WarehouseCreate):
    pass
