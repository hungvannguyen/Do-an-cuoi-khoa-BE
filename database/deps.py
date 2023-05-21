from datetime import datetime

import jwt
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from constants import Const
from database.db import SessionLocal, engine
from schemas.token import TokenPayload
from security.security import Authorization, check_authenticated


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: str = Depends(Authorization)) -> TokenPayload:
    try:
        token = check_authenticated(authorization)
        payload = jwt.decode(token, Const.SECRET_KEY, algorithms=Const.SECURITY_ALGORITHM)
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
    except(jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )
    return TokenPayload(**payload)


def get_admin_user(authorization: str = Depends(Authorization)) -> TokenPayload:
    try:
        token = check_authenticated(authorization)
        payload = jwt.decode(token, Const.SECRET_KEY, algorithms=Const.SECURITY_ALGORITHM)
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
        admin = TokenPayload(**payload)
        if admin.role_id == 1:
            return admin
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")
    except(jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORIZED"
        )