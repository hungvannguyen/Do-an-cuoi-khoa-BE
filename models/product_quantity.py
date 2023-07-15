from sqlalchemy import Column, Integer, String, Boolean, BigInteger, TEXT, Float

from models.BaseModel import BaseDBModel
from database.db import Base


class ProductQuantity(Base):
    __tablename__ = "product_quantity"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    prd_id = Column(BigInteger)
    import_price = Column(Float)
    quantity = Column(Integer, default=1)
