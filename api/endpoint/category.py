import os

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_category import crud_category
from schemas.category import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/all")
def get_all_category(db: Session = Depends(deps.get_db)):
    return crud_category.get_all_category(db)


@router.get("/{cat_id}")
def get_category_by_id(cat_id: int, db: Session = Depends(deps.get_db)):
    return crud_category.get_category_by_id(id=cat_id, db=db)


@router.post("/add")
def create_category(request: CategoryCreate, db: Session = Depends(deps.get_db),
                    token: TokenPayload = Depends(deps.get_employee_user)):
    return crud_category.create_category(request=request, db=db, admin_id=token.id)


@router.put("/update/{cat_id}")
def update_category(request: CategoryUpdate, cat_id: int, db: Session = Depends(deps.get_db),
                    token: TokenPayload = Depends(deps.get_employee_user)):
    return crud_category.update_category(request=request, id=cat_id, db=db, admin_id=token.id)


@router.delete("/delete/{cat_id}")
def delete_category(cat_id, db: Session = Depends(deps.get_db), token: TokenPayload = Depends(deps.get_admin_user)):
    return crud_category.delete_category(id=cat_id, db=db, admin_id=token.id)
