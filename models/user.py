from sqlalchemy import Column, Integer, String, Boolean, BigInteger, DateTime

# from models.BaseModel import BaseDBModel
from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    account = Column(String(255), unique=True, index=True)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    phone_number = Column(String(10), nullable=True)
    role_id = Column(Integer, nullable=False)
    insert_id = Column(BigInteger, nullable=False)
    insert_at = Column(DateTime, nullable=False)
    update_id = Column(BigInteger, nullable=False)
    update_at = Column(DateTime, nullable=False)
    delete_id = Column(BigInteger)
    delete_at = Column(DateTime, default=None)
    delete_flag = Column(Integer, index=True, default=0, nullable=False)
