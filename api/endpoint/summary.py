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
def get_total_income(mode: int = 0, year: int = 2023, db: Session = Depends(deps.get_db)):
    return CRUD_summary.total_income(db=db, mode=mode, year=year)


@router.get("/order_count")
def count_order(mode: int = 0, year: int = 2023, db: Session = Depends(deps.get_db)):
    return CRUD_summary.order_count(db=db, mode=mode, year=year)


@router.get("/order/count")
def count_by_user_id(user_id: int, db: Session = Depends(deps.get_db)):
    return CRUD_summary.order_count_by_user_id(user_id=user_id, db=db)


@router.get("/order/count/pending")
def count_by_user_id(db: Session = Depends(deps.get_db)):
    return CRUD_summary.order_count_by_status(db=db)


@router.get("/order/count/pending")
def count_pending_orders(db: Session = Depends(deps.get_db)):
    return CRUD_summary.get_total_pending_orders(db=db)


@router.get("/order/count/pending_refund")
def count_pending_refund_orders(db: Session = Depends(deps.get_db)):
    return CRUD_summary.get_total_pending_refund_orders(db=db)


@router.get("/top_customer")
def get_top_customers(db: Session = Depends(deps.get_db)):
    return CRUD_summary.get_top_customer(db=db)


@router.get("/low_quantity")
def get_low_quantity_products(db: Session = Depends(deps.get_db)):
    return CRUD_summary.get_low_quantity_products(db=db)
