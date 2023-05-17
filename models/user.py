from sqlalchemy import Column, Integer, String, Boolean

from models.BaseModel import BaseDBModel
from database.db import Base


class User(Base, BaseDBModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    account = Column(String(255), unique=True, index=True)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    phone_number = Column(String(10), nullable=True)
    role_id = Column(Integer, nullable=False, default=99)

