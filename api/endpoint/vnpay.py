from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_cart import crud_cart
from schemas.cart import *
from schemas.token import TokenPayload
from database import deps
from vnpay_python import forms, views

router = APIRouter()


@router.post("/create")
def create_vnpay_url(request: forms.PaymentForm):
    return views.payment(request=request)
