from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class User(Base, BaseDBModel):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    account = Column(String(255), index=True)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(10), nullable=True)
    role_id = Column(Integer, nullable=False, default=99)
    is_confirmed = Column(Integer, default=0)

