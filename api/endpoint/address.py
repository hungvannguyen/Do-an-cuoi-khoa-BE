import os

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_address import crud_address
from schemas.address import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/")
def get_address_by_user_id(db: Session = Depends(deps.get_db),
                           token: TokenPayload = Depends(deps.get_current_user)):
    data_db = crud_address.get_address_by_user_id(user_id=token.id, db=db)
    if not data_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User ID #{token.id} chưa có Địa chỉ nào")
    return data_db


@router.post("/create")
def create_address(request: AddressCreate, db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_current_user)):
    return crud_address.create_address(request=request, db=db, user_id=token.id)


@router.put("/update/")
def update_address(request: AddressUpdate, db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_current_user)):
    return crud_address.update_address(request=request, db=db, user_id=token.id)


@router.delete("/delete/{user_id}")
def delete_address(user_id: int, db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_admin_user)):
    return crud_address.delete_address(user_id=user_id, db=db, admin_id=token.id)
