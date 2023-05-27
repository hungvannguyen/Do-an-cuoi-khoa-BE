from sqlalchemy import Column, Integer, String, Boolean, BigInteger, TEXT

from models.BaseModel import BaseDBModel
from database.db import Base


class Product(Base, BaseDBModel):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    cat_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=1)
    img_url = Column(String(255), nullable=True)
    status = Column(Integer, default=1)
    description = Column(TEXT, nullable=True)
