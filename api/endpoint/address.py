import os
from typing import Any

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import crud.api_add
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_address import crud_address
from schemas.address import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/")
def get_addresses_by_user_id(db: Session = Depends(deps.get_db),
                           token: TokenPayload = Depends(deps.get_current_user)):
    data_db = crud_address.get_address_info_by_user_id(user_id=token.id, db=db)
    if not data_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User ID #{token.id} chưa có Địa chỉ nào")
    return data_db


@router.get("/detail")
def get_detail_by_user_id(user_id: int, db: Session = Depends(deps.get_db)):
    return crud_address.get_detail_address_by_user_id(user_id=user_id, db=db)


@router.get("/city/all")
def get_all_city(db: Session = Depends(deps.get_db),
                 token: TokenPayload = Depends(deps.get_current_user)):
    return crud_address.get_all_cities(db=db)


@router.get("/district/{city_id}")
def get_all_districts(city_id: int, db: Session = Depends(deps.get_db),
                      token: TokenPayload = Depends(deps.get_current_user)):
    return crud_address.get_all_districts(city_id=city_id, db=db)


@router.get("/ward/{city_id}/{district_id}")
def get_all_wards(city_id: int, district_id: int, db: Session = Depends(deps.get_db),
                  token: TokenPayload = Depends(deps.get_current_user)):
    return crud_address.get_all_wards(city_id=city_id, district_id=district_id, db=db)


@router.post("/create")
def create_address(request: AddressCreate, db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_current_user)):
    return crud_address.create_address(request=request, db=db, user_id=token.id)


@router.post("/update")
def update_address(address_id: int, request: AddressUpdate, db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_current_user)):
    return crud_address.update_address(address_id=address_id, request=request, db=db, user_id=token.id)


@router.delete("/delete")
def delete_address(address_id: int, db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_current_user)):
    return crud_address.delete_address(user_id=token.id, address_id=address_id, db=db)


@router.post("/abc")
def abc(db: Session = Depends(deps.get_db)):
    data = crud.api_add.data_api
    return crud_address.abcd(data, db)


@router.delete("/sample/del")
def delete_sample(db: Session = Depends(deps.get_db)):
    return crud_address.delete_address_sample(db=db)
