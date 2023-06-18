from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Log(Base, BaseDBModel):
    __tablename__ = "logs"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    type = Column(String(50), nullable=False)
    target = Column(String(255))
    comment = Column(String(255))
    status = Column(String(50))
