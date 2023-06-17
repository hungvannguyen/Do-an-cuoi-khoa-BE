import os

from fastapi import Depends, UploadFile, File, APIRouter, status
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import schemas.user
from crud import CRUD_mail
from schemas.mail import CodeConfirm
from security.security import verify_password
from fastapi.encoders import jsonable_encoder
from crud.CRUD_user import crud_user
from schemas.user import UserRegis, UserInfo, UserLogin, UserUpdatePassword, UserUpdateInfo
from schemas.token import TokenPayload
from database import deps

router = APIRouter()


@router.post("/regis")
def create_user(request: UserRegis, db: Session = Depends(deps.get_db)):
    return crud_user.create_user(db=db, request=request)


@router.post("/admin/{role_id}")
def create_admin(request: UserRegis, role_id: int, db: Session = Depends(deps.get_db)):
    return crud_user.create_admin(db=db, request=request, role_id=role_id)


@router.post("/login")
def login(request: UserLogin, db: Session = Depends(deps.get_db)):
    token, role_id = crud_user.login(db=db, account=request.account, password=request.password)
    return {
        'token': token,
        'role_id': role_id
    }


@router.put("/password/update")
def update_password(request: UserUpdatePassword, db: Session = Depends(deps.get_db),
                    token: TokenPayload = Depends(deps.get_current_user)):
    user_db = crud_user.get_user_by_id(db, token.id)
    current_user = jsonable_encoder(user_db)
    current_password = request.current_password
    if not verify_password(current_password, current_user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sai mật khẩu")
    if not request.password == request.password_repeat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mật khẩu không khớp")
    return crud_user.update_password(token.id, request.password, db)


@router.get("/confirm/{email}")
def confirm_email(email: str, db: Session = Depends(deps.get_db)):
    return crud_user.confirm_email(email=email, db=db)


@router.post("/confirm_code")
def confirm_code(request: CodeConfirm, db: Session = Depends(deps.get_db)):
    return crud_user.confirm_code(request=request, db=db)


@router.get("/role/all")
def get_all_roles(db: Session = Depends(deps.get_db), token: TokenPayload = Depends(deps.get_admin_user)):
    return crud_user.get_all_roles(db=db)


@router.get("/password/reset/{account}")
def reset_password(account, db: Session = Depends(deps.get_db), token: TokenPayload = Depends(deps.get_admin_user)):
    return crud_user.reset_password(db, account, token.role_id)


@router.get("/info", response_model=schemas.user.UserInfo)
def get_user_info(db: Session = Depends(deps.get_db), token: TokenPayload = Depends(deps.get_current_user)):
    return crud_user.get_user_info(db=db, id=token.id)


@router.post("/update")
def update_user_info(request: UserUpdateInfo, db: Session = Depends(deps.get_db),
                     token: TokenPayload = Depends(deps.get_current_user)):
    return crud_user.update_info(request=request, db=db, user_id=token.id)
