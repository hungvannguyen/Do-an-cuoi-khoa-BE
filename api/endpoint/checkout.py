import os

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
import crud.CRUD_checkout
from schemas.category import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/checkout")
def get_checkout_info(db: Session = Depends(deps.get_db), token: TokenPayload = Depends(deps.get_current_user)):
    return crud.CRUD_checkout.get_checkout_info(db=db, user_id=token.id)
