from typing import Optional

from pydantic import BaseModel
from schemas.Default import Config


class UserBase(BaseModel, Config):
    id: int
    name: Optional[str]


class UserInfo(UserBase):
    email: Optional[str]
    phone_number: Optional[str]
    role_id: int


class UserRegis(BaseModel):
    account: str
    password: str


class UserUpdatePassword(BaseModel):
    current_password: str
    password: str
    password_repeat: str


class UserLogin(UserRegis):
    pass
