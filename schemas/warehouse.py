from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class WarehouseBase(BaseModel, Config):
    id: int


class WarehouseCreate(BaseModel):

    city_id: Optional[int]
    district_id: Optional[int]
    ward: Optional[int]
    detail: Optional[str]


class WarehouseUpdate(WarehouseCreate):
    pass
