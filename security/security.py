from datetime import datetime, timedelta, time
from typing import Union, Any, Optional
from fastapi.security.utils import get_authorization_scheme_param
import jwt
from fastapi import HTTPException, status
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext

from constants import Const


Authorization = APIKeyHeader(name='Authorization')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def check_authenticated(
        authorization: str
) -> Optional[str]:
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return param


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def gen_token(user) -> Any:
    expire = datetime.now() + timedelta(
        seconds=3600 * 24
    )
    to_encode = {
        "exp": expire,
        "name": user['name'],
        "address": user['address'],
        "phone_number": user['phone_number'],
        "role_id": user['role_id']
    }
    encoded_token = jwt.encode(to_encode, Const.SECRET_KEY, Const.SECURITY_ALGORITHM)
    return encoded_token
