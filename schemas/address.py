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

    city: Optional[int]
    district: Optional[int]
    ward: Optional[int]
    detail: Optional[str]


class AddressUpdate(AddressCreate):
    pass
