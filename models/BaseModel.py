# import Datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger


class BaseDBModel:
    insert_id = Column(BigInteger, nullable=False)
    insert_at = Column(DateTime, nullable=False)
    update_id = Column(BigInteger, nullable=False)
    update_at = Column(DateTime, nullable=False)
    delete_id = Column(BigInteger)
    delete_at = Column(DateTime, default=None)
    delete_flag = Column(Integer, index=True, default=0, nullable=False)
