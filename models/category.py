from sqlalchemy import Column, Integer, String, Boolean, BigInteger, TEXT

from models.BaseModel import BaseDBModel
from database.db import Base


class Category(Base, BaseDBModel):
    __tablename__ = "categories"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    cat_name = Column(String(255), nullable=False)
    cat_description = Column(TEXT, nullable=True)
