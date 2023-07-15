from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, BigInteger, TEXT, DateTime, FLOAT

from models.BaseModel import BaseDBModel
from database.db import Base


class ProductImportDetail(Base, BaseDBModel):
    __tablename__ = "product_import_detail"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    product_import_id = Column(BigInteger)
    prd_id = Column(BigInteger)
    quantity = Column(Integer)
    import_price = Column(FLOAT)
    name = Column(String(255))
