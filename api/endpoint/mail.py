import os
from typing import Any

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import crud.api_add
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud import CRUD_mail
from schemas.mail import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.post("/confirm_email")
def create_confirm_mail(request: MailConfirm, db: Session = Depends(deps.get_db)):
    return CRUD_mail.create_confirm_mail(mail_to=request.mail_to, db=db)


@router.post("/send_confirm_code")
def create_confirm_code(request: CodeConfirmCreate, db: Session = Depends(deps.get_db)):
    return CRUD_mail.create_confirm_code_email(account=request.account, db=db)


@router.post("/order_details")
def create_order_details_email(order_id: int, db: Session = Depends(deps.get_db)):
    return CRUD_mail.create_order_detail_email(order_id=order_id, db=db)
