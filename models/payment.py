from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime

from models.BaseModel import BaseDBModel
from database.db import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    payment_type_id = Column(BigInteger, nullable=False)
    txnRef = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False, default=99)
    bankCode = Column(String(50), nullable=True)
    transactionNo = Column(String(100), nullable=True)
    insert_at = Column(DateTime, nullable=False, default=datetime.now())
