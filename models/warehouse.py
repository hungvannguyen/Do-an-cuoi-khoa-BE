from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Warehouse(Base, BaseDBModel):
    __tablename__ = "warehouses"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    city_id = Column(BigInteger, nullable=False)
    district_id = Column(BigInteger, nullable=False)
    ward_id = Column(BigInteger, nullable=False)
    detail = Column(String(255), nullable=False)
