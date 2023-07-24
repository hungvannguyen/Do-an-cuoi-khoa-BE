from __future__ import annotations

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud import CRUD_summary
from schemas.product import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/total_income")
def get_total_income(db: Session = Depends(deps.get_db)):
    return CRUD_summary.total_income(db=db)


@router.get("/order_count")
def count_order(year: int = None, db: Session = Depends(deps.get_db)):
    return CRUD_summary.order_count(db=db, year=year, month=0)


@router.get("/order/count")
def count_by_user_id(user_id: int, db: Session = Depends(deps.get_db)):
    return CRUD_summary.order_count_by_user_id(user_id=user_id, db=db)
