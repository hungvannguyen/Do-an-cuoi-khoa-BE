from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class UserBase(BaseModel, Config):
    id: int
    name: Optional[str]


class UserInfo(UserBase):
    address: Optional[str]
    phone_number: Optional[str]
    role_id: int


class UserRegis(BaseModel):
    account: str
    password: str


class UserLogin(UserRegis):
    pass
