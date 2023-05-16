import os

from fastapi import FastAPI, Depends, UploadFile, File
from passlib.context import CryptContext

from api.api import api_router

app = FastAPI()

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

