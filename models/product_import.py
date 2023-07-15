from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, BigInteger, TEXT, DateTime, FLOAT

from models.BaseModel import BaseDBModel
from database.db import Base


class ProductImport(Base, BaseDBModel):
    __tablename__ = "product_import"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    user_id = Column(BigInteger, nullable=False, default=1)
    import_at = Column(DateTime, nullable=False, default=datetime.now())
    import_quantity = Column(Integer)
    total_import_price = Column(FLOAT)
