from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_payment import crud_payment
from schemas.payment import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/info/{id}")
def get_payment_info(id: int, db: Session = Depends(deps.get_db),
                     token: TokenPayload = Depends(deps.get_current_user)):
    return crud_payment.get_payment_by_id(id=id, db=db)


@router.post("/add")
def add_payment(request: PaymentCreate, db: Session = Depends(deps.get_db),
                token: TokenPayload = Depends(deps.get_current_user)):
    return crud_payment.add_payment(request=request, db=db, user_id=token.id)


@router.get("/update")
def update_payment(payment_id: int, payment_status: int, bankCode: str = None, transactionNo: str = None,
                   db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_current_user)):
    return crud_payment.update_payment(payment_id, payment_status, bankCode, transactionNo, db=db, user_id=token.id)


@router.get("/update/cod")
def complete_cod_payment(payment_id: int, db: Session = Depends(deps.get_db)):
    return crud_payment.complete_cod_payment(payment_id=payment_id, db=db)
