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
from upload.upload import uploadFile

router = APIRouter()


@router.post("/upload")
def upload(file: UploadFile = File(...)):
    filename = uploadFile(file)
    return {'filename': filename}
