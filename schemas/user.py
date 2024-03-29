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
    email: str
    name: str
    phone_number: str
    password: str
    confirm_password: str


class AdminRegis(UserRegis):
    pass

class UserUpdateInfo(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]


class UserUpdatePassword(BaseModel):
    current_password: str
    password: str
    password_repeat: str


class UserLogin(BaseModel):
    account: str
    password: str


class UserResetPassword(BaseModel):
    password: str
    password_repeat: str
