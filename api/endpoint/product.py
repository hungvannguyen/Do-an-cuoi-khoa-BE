from __future__ import annotations

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_product import crud_product
from schemas.product import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/all")
def get_all(page: int = 1, db: Session = Depends(deps.get_db)):
    data = crud_product.get_all_products(page=page, db=db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không có sản phẩm")
    return data


@router.get("/all/active")
def get_all_active(page: int = 1, db: Session = Depends(deps.get_db)):
    data = crud_product.get_all_active_products(page=page, db=db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không có sản phẩm")
    return data


@router.get("/sale")
def get_sale_products(page: int = 1, sort: int = 0, db: Session = Depends(deps.get_db)):
    print(sort)
    return crud_product.get_sale_products(page=page, db=db)


@router.get("/new")
def get_new_products(page: int = 1, db: Session = Depends(deps.get_db)):
    return crud_product.get_new_products(page=page, db=db)


@router.get("/best-seller")
def get_best_seller_products(db: Session = Depends(deps.get_db)):
    pass


@router.get("/category/{cat_id}")
def get_products_by_cat_id(cat_id: int, page: int = 1, db: Session = Depends(deps.get_db)):
    return crud_product.get_by_cat_id(cat_id=cat_id, page=page, db=db)


@router.get("/{id}")
def get_product_by_id(id: int, db: Session = Depends(deps.get_db)):
    return crud_product.get_product_by_id(id=id, db=db)


@router.post("/add")
def create_product(request: ProductCreate, db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_employee_user)):
    return crud_product.create_product(request=request, db=db, admin_id=token.id)


@router.put("/update/{id}")
def update_product(id: int, request: ProductUpdate, db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_employee_user)):
    return crud_product.update_product(id=id, request=request, db=db, admin_id=token.id)
