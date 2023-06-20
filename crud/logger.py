import json
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status as code_status
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
    return {
        'success'
    }


def get_log(type, target, status, id, db: Session):
    obj = db.query(Log)

    if type != None:
        type = str(type)
        type = type.upper()
        obj = obj.filter(Log.type == type)
    if target != None:
        target = str(target)
        target = target.upper()
        obj = obj.filter(
            Log.target == target
        )
    if status != None:
        status = str(status)
        status = status.upper()
        obj = obj.filter(Log.status == status)
    if id != None:
        obj = obj.filter(Log.insert_id == id)

    obj = obj.all()
    if not obj:
        raise HTTPException(status_code=code_status.HTTP_404_NOT_FOUND, detail=f"Không có Log phù hợp")

    return obj
