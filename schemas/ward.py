from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class WardBase(BaseModel, Config):
    id: Optional[int]


class WardInfo(WardBase):
    city_id: Optional[int]
    district_id: Optional[int]
    name: Optional[str]


class WardCreate(BaseModel):
    city_id: Optional[int]
    district_id: Optional[int]
    name: Optional[str]
