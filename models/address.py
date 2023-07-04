from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Address(Base, BaseDBModel):
    __tablename__ = "addresses"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    user_id = Column(BigInteger, nullable=False)
    city_id = Column(BigInteger, nullable=False)
    district_id = Column(BigInteger, nullable=False)
    ward_id = Column(BigInteger, nullable=False)
    detail = Column(String(255), nullable=False)
    is_default = Column(Integer, default=99)
