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

router = APIRouter()


@router.get("/all")
def get_cart(db: Session = Depends(deps.get_db), token: TokenPayload = Depends(deps.get_current_user)):
    return crud_cart.get_cart(user_id=token.id, db=db)


@router.post("/add")
def create_cart(request: CartCreate, db: Session = Depends(deps.get_db),
                token: TokenPayload = Depends(deps.get_current_user)):
    return crud_cart.add_to_cart(request=request, db=db, user_id=token.id)


@router.put("/update/{prd_id}/quantity/{quantity}")
def update_cart(prd_id: int, quantity: int, db: Session = Depends(deps.get_db),
                token: TokenPayload = Depends(deps.get_current_user)):
    return crud_cart.update_cart(prd_id=prd_id, quantity=quantity, db=db, user_id=token.id)


@router.delete("/delete/{prd_id}")
def delete_cart(prd_id: int, db: Session = Depends(deps.get_db),
                token: TokenPayload = Depends(deps.get_current_user)):
    return crud_cart.delete_cart(prd_id=prd_id, db=db, user_id=token.id)
