from sqlalchemy import Column, Integer, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Cart(Base, BaseDBModel):
    __tablename__ = "carts"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    user_id = Column(BigInteger, nullable=False)
    prd_id = Column(BigInteger, nullable=False)
    quantity = Column(Integer, default=1)
    