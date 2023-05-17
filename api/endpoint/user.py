import os

from fastapi import Depends, UploadFile, File, APIRouter
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from crud.CRUD_user import crud_user
import schemas.user
from database import deps
from schemas.login import LoginRequest
from security.security import gen_token, check_token
from upload.upload import uploadFile

router = APIRouter()


@router.post("/regis")
def create_user(request: schemas.user.UserRegis, db: Session = Depends(deps.get_db)):
    return crud_user.create_user(db=db, request=request)

