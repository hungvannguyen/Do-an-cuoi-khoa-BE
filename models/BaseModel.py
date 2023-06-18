# import Datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger
from datetime import datetime


class BaseDBModel:
    insert_id = Column(BigInteger, nullable=False, default=1)
    insert_at = Column(DateTime, nullable=False, default=datetime.now())
    update_id = Column(BigInteger, nullable=False, default=1)
    update_at = Column(DateTime, nullable=False, default=datetime.now())
    delete_id = Column(BigInteger, nullable=True)
    delete_at = Column(DateTime, nullable=True)
    delete_flag = Column(Integer, index=True, default=0, nullable=False)
