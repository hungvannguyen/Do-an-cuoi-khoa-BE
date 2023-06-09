import os

from fastapi import Depends, UploadFile, File, APIRouter
from passlib.context import CryptContext

import schemas.token
from schemas.login import LoginRequest
from security.security import gen_token
from database import deps
from upload.upload import uploadFile, return_img

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
fake_db = []
router = APIRouter()


def get_hashed_pass(password: str):
    return pwd_context.hash(password)


@router.post("/regis")
def regis(request: LoginRequest):
    hashed_pass = get_hashed_pass(request.password)
    obj_in = {
        "username": request.username,
        "hashedpassword": hashed_pass
    }
    fake_db.append(obj_in)
    print(fake_db[0].get('username'))


@router.post("/login")
def login(request: LoginRequest):
    if request.username == fake_db[0].get('username') and pwd_context.verify(request.password,
                                                                             fake_db[0].get('hashedpassword')):
        return gen_token(request.username)
    return {"Not"}


@router.get("/test")
def test(token: schemas.token.TokenPayload = Depends(deps.get_current_user)):
    return {
        'user': token
    }


@router.post("/upload")
def upload(file: UploadFile = File(...)):
    filename = uploadFile(file)
    return {"filename": filename}


@router.get("/img")
def get_img(name: str):
    return return_img(name=name)



@router.post("/test1")
def test1():
    return {
        "result": [{
            "ab": "a",
            "cd": "c"
        },
            {
                "ab1": "a",
                "cd1": "c"
            }]
    }


@router.post("/test2/{var}")
def test2(var: str):
    return {
        "result": [var, var, var]
    }
