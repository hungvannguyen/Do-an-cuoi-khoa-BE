from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class District(Base):
    __tablename__ = "districts"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    city_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=False)
