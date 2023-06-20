from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.warehouse import WarehouseCreate
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


@router.post("/add")
def create_warehouse(request: WarehouseCreate, db: Session = Depends(deps.get_db),
                     token: TokenPayload = Depends(deps.get_admin_user)):
    return crud_warehouse.create_warehouse(request=request, db=db, admin_id=token.id)

