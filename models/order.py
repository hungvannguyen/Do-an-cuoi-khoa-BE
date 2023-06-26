from sqlalchemy import Column, Integer, String, Boolean, BigInteger, TEXT, Float

from models.BaseModel import BaseDBModel
from database.db import Base


class Order(Base, BaseDBModel):
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
