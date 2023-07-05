from sqlalchemy import Column, Integer, String, Boolean, BigInteger, FLOAT

from models.BaseModel import BaseDBModel
from database.db import Base


class Order_Product(Base, BaseDBModel):
    __tablename__ = "order_product"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    order_id = Column(BigInteger, nullable=False)
    product_id = Column(BigInteger, nullable=False)
    name = Column(String(255))
    img_url = Column(String(255))
    quantity = Column(Integer, default=1)
    import_price = Column(FLOAT)
    price = Column(FLOAT)
