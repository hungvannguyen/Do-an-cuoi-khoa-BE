import os

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_order import crud_order
from schemas.order import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/info/{order_id}")
def get_order_by_id(order_id: int, db: Session = Depends(deps.get_db),
                    token: TokenPayload = Depends(deps.get_current_user)):
    return crud_order.get_order_by_id(order_id=order_id, db=db, user_id=token.id)


@router.get("/all")
def get_all_order(page: int = 1, order_status: int = None, db: Session = Depends(deps.get_db),
                  token: TokenPayload = Depends(deps.get_current_user)):
    return crud_order.get_all_orders_by_user_id(page=page, order_status=order_status, db=db, user_id=token.id)


@router.get("/admin/all")
def get_all_order_for_admin(page: int = 1, order_status: int = None, db: Session = Depends(deps.get_db),
                            token: TokenPayload = Depends(deps.get_employee_user)):
    return crud_order.get_all_orders(page=page, order_status=order_status, db=db, admin_id=token.id)


@router.post("/add")
def add_order(request: OrderCreate, db: Session = Depends(deps.get_db),
              token: TokenPayload = Depends(deps.get_current_user)):

    abc = 1

    return crud_order.add_order(request=request, db=db, user_id=token.id, email=token.email)


@router.get("/update")
def update_order_status(order_status: int, order_id: int, db: Session = Depends(deps.get_db),
                        token: TokenPayload = Depends(deps.get_current_user)):
    return crud_order.update_order_status(order_status=order_status, order_id=order_id, db=db, user_id=token.id)


@router.delete("/cancel")
def cancel_order(order_id: int, db: Session = Depends(deps.get_db),
                 token: TokenPayload = Depends(deps.get_current_user)):
    return crud_order.cancel_order(order_id=order_id, db=db, user_id=token.id)
