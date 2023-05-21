from fastapi import APIRouter

from api.endpoint import (
    login_regis,
    user,
    category
)

api_router = APIRouter()

api_router.include_router(login_regis.router, prefix="/v1", tags=["TÉT"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(category.router, prefix="/category", tags=["Category"])
