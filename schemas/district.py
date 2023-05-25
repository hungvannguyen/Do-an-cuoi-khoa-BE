from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class DistrictBase(BaseModel, Config):
    id: Optional[int]


class DistrictInfo(DistrictBase):
    city_id: Optional[str]
    name: Optional[str]


class DistrictCreate(BaseModel):
    city_id: Optional[str]
    name: Optional[str]
