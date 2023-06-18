import json
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.log import Log
from schemas.address import AddressInfo, AddressCreate, AddressUpdate
from crud.base import CRUDBase
from constants import Const
from security.security import hash_password, verify_password


def log(type, target, comment, status, id, db: Session):
    obj = Log()
    obj.type = type
    obj.target = target
    obj.comment = comment
    obj.status = status
    obj.insert_id = id
    obj.insert_at = datetime.now()
    obj.update_at = datetime.now()
    obj.update_id = id
    obj.delete_flag = Const.DELETE_FLAG_NORMAL

    db.add(obj)
    db.commit()
    db.refresh(obj)
