from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Address(Base, BaseDBModel):
    __tablename__ = "addresses"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    user_id = Column(BigInteger, nullable=False)
    district = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    ward = Column(String(255), nullable=False)
    detail = Column(String(255), nullable=False)
