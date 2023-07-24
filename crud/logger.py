import json
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status as code_status
from fastapi.encoders import jsonable_encoder
from models.log import Log
from models.user import User
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


def get_log(type, target, status, id, sort, page, row_per_page, date_from, date_to, db: Session):
    obj = db.query(Log)

    if type != None:
        type = str(type)
        type = type.upper()
        obj = obj.filter(Log.type == type)

    if target != None:
        target = str(target)
        target = target.upper()
        obj = obj.filter(Log.target == target)

    if status != None:
        status = str(status)
        status = status.upper()
        obj = obj.filter(Log.status == status)

    if id != None:
        obj = obj.filter(Log.insert_id == id)

    if sort == 'asc':
        obj = obj.order_by(Log.insert_at.asc())
    elif sort == 'desc':
        obj = obj.order_by(Log.insert_at.desc())

    if date_from != None:
        obj = obj.filter(Log.insert_at >= date_from)

    if date_to != None:
        obj = obj.filter(Log.insert_at <= date_to)

    total_logs = obj.count()
    total_page = int(total_logs / row_per_page)
    if total_logs % row_per_page > 0:
        total_page += 1
    current_page = page
    if current_page <= 0:
        current_page = 1
    if current_page > total_page > 0:
        current_page = total_page

    start = (current_page - 1) * row_per_page
    obj = obj.offset(start).limit(row_per_page).all()

    for item in obj:
        user_id = item.insert_id

        user_db = db.query(User).filter(
            User.id == user_id
        ).first()

        name = user_db.name

        setattr(item, 'name', name)

    if not obj:
        raise HTTPException(status_code=code_status.HTTP_404_NOT_FOUND, detail=f"Không có Log phù hợp")

    return {
        'data': obj,
        'current_page': current_page,
        'total_page': total_page
    }
