from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Payment(Base, BaseDBModel):
    __tablename__ = "payments"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    payment_type_id = Column(BigInteger, nullable=False)
    status = Column(Integer, nullable=False)
