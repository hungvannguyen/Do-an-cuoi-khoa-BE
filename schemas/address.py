from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class AddressBase(BaseModel, Config):
    id: Optional[int]
    user_id: Optional[int]


class AddressInfo(AddressBase):
    district: Optional[str]
    ward: Optional[str]
    city: Optional[str]
    detail: Optional[str]


class AddressCreate(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
    city_id: Optional[int]
    district_id: Optional[int]
    ward_id: Optional[int]
    detail: Optional[str]


class AddressUpdate(AddressCreate):
    pass
