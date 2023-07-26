import os

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_import_product import crud_import_product
from schemas.product_import import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.post("/import")
def import_products(request: ProductImportCreate, db: Session = Depends(deps.get_db)):
    return crud_import_product.create_import_invoice(request=request, db=db, admin_id=1)


@router.get("/all")
def get_all_invoices(db: Session = Depends(deps.get_db)):
    return crud_import_product.get_inport_invoice(db=db)


@router.get("/{id}")
def get_invoice_by_id(id: int, db: Session = Depends(deps.get_db)):
    return crud_import_product.get_import_invoice_by_id(id=id, db=db)
