from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_paymentType import crud_paymentType
from schemas.paymentType import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/all")
def get_all_payment_type(db: Session = Depends(deps.get_db)):
    return crud_paymentType.get_all_payment_type(db=db)


@router.get("/{paymentType_id}")
def get_payment_type(paymentType_id: int, db: Session = Depends(deps.get_db)):
    return crud_paymentType.get_payment_type(paymentType_id=paymentType_id, db=db)


@router.post("/add")
def create_payment_type(request: PaymentTypeCreate, db: Session = Depends(deps.get_db),
                        token: TokenPayload = Depends(deps.get_employee_user)):
    return crud_paymentType.create_payment_type(request=request, db=db, admin_id=token.id)
