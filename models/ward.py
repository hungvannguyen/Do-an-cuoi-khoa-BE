from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Ward(Base):
    __tablename__ = "wards"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    city_id = Column(BigInteger, nullable=False)
    district_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=False)
