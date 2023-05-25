from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class City(Base, BaseDBModel):
    __tablename__ = "cities"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    name = Column(String(255), nullable=False)
    