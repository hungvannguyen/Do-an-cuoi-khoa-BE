from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Role(Base, BaseDBModel):
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    name = Column(String(255))
