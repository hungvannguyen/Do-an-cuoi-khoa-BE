import os
from datetime import datetime, date

# from click import DateTime
from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
import crud.CRUD_checkout
from crud.CRUD_cart import crud_cart
from schemas.category import *
from schemas.token import TokenPayload
from database import deps
from crud.logger import get_log

router = APIRouter()


@router.get("/all")
def get_logs(type: str = None, target: str = None, status: str = None, id: int = None, sort: str = 'asc',
             page: int = 1, row_per_page: int = 100,
             date_from: date = None, date_to: date = None,
             db: Session = Depends(deps.get_db)):
    return get_log(type=type, target=target, status=status, id=id, sort=sort, page=page, row_per_page=row_per_page,
                   date_from=date_from, date_to=date_to, db=db)
