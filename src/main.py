
from fastapi import FastAPI
import models
from api.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine


origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5000",

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

