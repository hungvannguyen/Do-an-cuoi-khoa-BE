import os

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
def get_logs(type: str = None, target: str = None, status: str = None, id: int = None,
             db: Session = Depends(deps.get_db)):
    return get_log(type=type, target=target, status=status, id=id, db=db)
