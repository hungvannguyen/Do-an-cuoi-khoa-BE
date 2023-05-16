from api.endpoint import login_regis
from fastapi import APIRouter

api_router = APIRouter()


api_router.include_router(login_regis.router, prefix="/v1", tags=["abc"])


