from datetime import datetime, timedelta, time
from typing import Union, Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '6EF6B30F9E557F948C402C89002C7C8A'

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def gen_token(username: Union[str, Any]) -> Any:
    expire = datetime.now() + timedelta(
        seconds=3600 * 24 * 3
    )
    to_encode = {
        "exp": expire,
        "username": username
    }
    encoded_token = jwt.encode(to_encode, SECRET_KEY, SECURITY_ALGORITHM)
    return encoded_token


def check_token(credentials=Depends(reusable_oauth2)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=SECURITY_ALGORITHM)
        print(payload)
        if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('username')
    except(jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=403,
            detail="Not validated"
        )
