from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Address(Base):
    __tablename__ = "user_info"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    user_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(10), nullable=False)
    city_id = Column(BigInteger, nullable=False)
    district_id = Column(BigInteger, nullable=False)
    ward_id = Column(BigInteger, nullable=False)
    detail = Column(String(255), nullable=False)
    is_default = Column(Integer, default=99)
    delete_flag = Column(Integer, index=True, default=0, nullable=False)
