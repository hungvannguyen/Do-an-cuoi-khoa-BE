import os

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import gen_token

from crud.CRUD_user import crud_user
from schemas.user import UserRegis, UserInfo, UserLogin
from database import deps

router = APIRouter()


@router.post("/regis")
def create_user(request: UserRegis, db: Session = Depends(deps.get_db)):
    return crud_user.create_user(db=db, request=request)


@router.post("/login")
def login(request: UserLogin, db: Session = Depends(deps.get_db)):
    return crud_user.login(db=db, account=request.account, password=request.password)
