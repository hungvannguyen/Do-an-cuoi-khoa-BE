from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, BigInteger, TEXT, Float, DateTime

from models.BaseModel import BaseDBModel
from database.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    user_id = Column(BigInteger, nullable=False)
    payment_id = Column(BigInteger, nullable=False)
    total_price = Column(Float, nullable=False)
    name = Column(String(255))
    phone_number = Column(String(10))
    email = Column(String(255))
    address = Column(String(255), nullable=False)
    note = Column(TEXT, nullable=True)
    status = Column(Integer, nullable=False, default=0)
    insert_id = Column(BigInteger, nullable=False, default=1)
    insert_at = Column(DateTime, nullable=False, default=datetime.now())
    update_id = Column(BigInteger, nullable=False, default=1)
    update_at = Column(DateTime, nullable=False, default=datetime.now())
