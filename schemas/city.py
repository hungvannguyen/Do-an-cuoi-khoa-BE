from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class CityBase(BaseModel, Config):
    id: Optional[int]


class CityInfo(CityBase):
    name: Optional[str]


class CityCreate(BaseModel):
    name: Optional[str]
