from fastapi import APIRouter

from .endpoint import (
    login_regis,

    )


api_router = APIRouter()


api_router.include_router(login_regis.router, prefix="/v1", tags=["abc"])


