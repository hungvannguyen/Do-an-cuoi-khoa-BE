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


@router.post("/auto_mail")
def create_confirm_mail(request: MailConfirm):
    return CRUD_mail.create_confirm_mail(mail_to=request.mail_to)
