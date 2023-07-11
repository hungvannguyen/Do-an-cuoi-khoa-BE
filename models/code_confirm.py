from sqlalchemy import Column, Integer, DateTime, String, Boolean, BigInteger

from models.BaseModel import BaseDBModel
from database.db import Base


class Code_Confirm(Base):
    __tablename__ = "code_confirm"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    user_id = Column(BigInteger, nullable=False)
    code = Column(String(10), nullable=False)
    expire_time = Column(DateTime, nullable=False)
    delete_flag = Column(Integer, index=True, default=0, nullable=False)
