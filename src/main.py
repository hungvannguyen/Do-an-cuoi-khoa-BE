import os

from fastapi import FastAPI, Depends, UploadFile, File
from passlib.context import CryptContext

from api.api import api_router
from security.security import check_token
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}", dependencies=[Depends(check_token)])
def say_hello(name: str):
    return {"message": f"Hello {name}"}

