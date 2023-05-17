import os

from fastapi import FastAPI, Depends, UploadFile, File
from passlib.context import CryptContext
import models
from api.api import api_router
from security.security import check_token
from fastapi.middleware.cors import CORSMiddleware
from database.db import SessionLocal, engine, Base


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

