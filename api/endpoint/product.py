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
def get_all(page: int = 1, sort: int = 0, min_price: int = 0, max_price: int = 0, db: Session = Depends(deps.get_db)):
    condition = {
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price
    }
    data = crud_product.get_all_products(page=page, condition=condition, db=db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không có sản phẩm")
    return data


@router.get("/all/active")
def get_all_active(page: int = 1, sort: int = 0, min_price: int = 0, max_price: int = 0,
                   db: Session = Depends(deps.get_db)):
    condition = {
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price
    }
    data = crud_product.get_all_active_products(page=page, condition=condition, db=db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không có sản phẩm")
    return data


@router.get("/sale")
def get_sale_products(page: int = 1, sort: int = 0, min_price: int = 0, max_price: int = 0,
                      db: Session = Depends(deps.get_db)):
    condition = {
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price
    }
    return crud_product.get_sale_products(page=page, condition=condition, db=db)


@router.get("/new")
def get_new_products(page: int = 1,
                     db: Session = Depends(deps.get_db)):
    return crud_product.get_new_products(page=page, db=db)


@router.get("/best-seller")
def get_best_seller_products(db: Session = Depends(deps.get_db)):
    return crud_product.get_best_seller_products(db=db)


@router.get("/category/{cat_id}")
def get_products_by_cat_id(cat_id: int, page: int = 1, sort: int = 0, min_price: int = 0, max_price: int = 0,
                           db: Session = Depends(deps.get_db)):
    condition = {
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price
    }
    return crud_product.get_by_cat_id(cat_id=cat_id, page=page, condition=condition, db=db)


@router.get("/search")
def search_products(keyword: str, page: int = 1, sort: int = 0, min_price: int = 0, max_price: int = 0,
                    db: Session = Depends(deps.get_db)):
    condition = {
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price
    }

    return crud_product.search_product(keyword=keyword, page=page, condition=condition, db=db)


@router.get("/admin/search")
def search_products_for_admin(keyword: str, page: int = 1, sort: int = 0, min_price: int = 0, max_price: int = 0,
                    db: Session = Depends(deps.get_db)):
    condition = {
        'sort': sort,
        'min_price': min_price,
        'max_price': max_price
    }

    return crud_product.search_product_for_admin(keyword=keyword, page=page, condition=condition, db=db)


@router.get("/{id}")
def get_product_by_id(id: int, db: Session = Depends(deps.get_db)):
    return crud_product.get_product_by_id(id=id, db=db)


@router.get("/import/all")
def get_all_for_import(db: Session = Depends(deps.get_db)):
    return crud_product.get_all_for_import(db=db)


@router.post("/add")
def create_product(request: ProductCreate, db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_employee_user)):
    return crud_product.create_product(request=request, db=db, admin_id=token.id)


@router.put("/update/quantity")
def update_quantity(request: ProductUpdateQuantity, db: Session = Depends(deps.get_db),
                    token: TokenPayload = Depends(deps.get_employee_user)):
    return crud_product.update_quantity(request=request.data, db=db)


@router.put("/update/{id}")
def update_product(id: int, request: ProductUpdate, db: Session = Depends(deps.get_db),
                   token: TokenPayload = Depends(deps.get_employee_user)):
    return crud_product.update_product(id=id, request=request, db=db, admin_id=token.id)

# @router.post("/add_quantity")
# def add_quantity(prd_id: int, quantity: int = 1, db: Session = Depends(deps.get_db)):
#     return crud_product.add_quantity(prd_id=prd_id, quantity=quantity, db=db, admin_id=1)
