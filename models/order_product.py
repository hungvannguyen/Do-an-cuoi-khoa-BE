from sqlalchemy import Column, Integer, String, Boolean, BigInteger, FLOAT

from models.BaseModel import BaseDBModel
from database.db import Base


class Order_Product(Base, BaseDBModel):
    __tablename__ = "order_product"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    order_id = Column(BigInteger, nullable=False)
    product_id = Column(BigInteger, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(FLOAT)
