from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Settings(Base, BaseDBModel):
    __tablename__ = "settings"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    banner_1 = Column(String(100), nullable=True)
    banner_2 = Column(String(100), nullable=True)
    banner_3 = Column(String(100), nullable=True)
    banner_4 = Column(String(100), nullable=True)
    banner_5 = Column(String(100), nullable=True)
    sale_banner = Column(String(100), nullable=True)
