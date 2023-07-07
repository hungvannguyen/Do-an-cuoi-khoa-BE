from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_setting import crud_setting
from schemas.setting import *
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.get("/all")
def get_settings(db: Session = Depends(deps.get_db)):
    return crud_setting.get_settings(db=db)


@router.put("/update")
def update_settings(request: SettingUpdate, db: Session = Depends(deps.get_db),
                    token: TokenPayload = Depends(deps.get_admin_user)):
    return crud_setting.update_settings(request=request, db=db, admin_id=token.id)
