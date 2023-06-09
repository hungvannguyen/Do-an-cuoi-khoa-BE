import os

from fastapi import FastAPI
import models
from api.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine
from fastapi.staticfiles import StaticFiles

origins = [
    "*"
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# app.mount(os.getcwd() + "/img/", StaticFiles(directory=os.getcwd() + "/img"), name="img")
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
