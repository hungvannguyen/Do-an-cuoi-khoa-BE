from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_warehouse import crud_warehouse
from schemas.product import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/info")
def get_warehouse_info(token: TokenPayload = Depends(deps.get_employee_user), db: Session = Depends(deps.get_db)):
    return crud_warehouse.get_warehouse_info(db=db)
