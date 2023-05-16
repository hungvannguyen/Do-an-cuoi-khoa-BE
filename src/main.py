import os

from fastapi import FastAPI, Depends, UploadFile, File
from passlib.context import CryptContext

from api.api import api_router
from security.security import check_token

app = FastAPI()

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}", dependencies=[Depends(check_token)])
def say_hello(name: str):
    return {"message": f"Hello {name}"}

