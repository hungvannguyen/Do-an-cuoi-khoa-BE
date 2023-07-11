from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime

from models.BaseModel import BaseDBModel
from database.db import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    type = Column(String(50), nullable=False)
    target = Column(String(255))
    comment = Column(String(255))
    status = Column(String(50))
    insert_id = Column(BigInteger, nullable=False, default=1)
    insert_at = Column(DateTime, nullable=False, default=datetime.now())
