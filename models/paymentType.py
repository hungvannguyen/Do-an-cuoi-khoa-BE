from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class PaymentType(Base, BaseDBModel):
    __tablename__ = "payment_types"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    name = Column(String(255), nullable=False)
