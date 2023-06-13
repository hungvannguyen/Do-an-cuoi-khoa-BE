from fastapi import APIRouter

from api.endpoint import (
    login_regis,
    user,
    category,
    address,
    mail,
    product,
    cart,
    image,
    checkout,
    warehouse,
    paymentType,
    payment,
    order,
    files
)

api_router = APIRouter()

# api_router.include_router(login_regis.router, prefix="/v1", tags=["TÉT"])
api_router.include_router(files.router, prefix="/file", tags=["FILES"])
api_router.include_router(user.router, prefix="/user", tags=["USER"])
api_router.include_router(category.router, prefix="/category", tags=["CATEGORY"])
api_router.include_router(address.router, prefix="/address", tags=["ADDRESS"])
api_router.include_router(warehouse.router, prefix="/warehouse", tags=['WAREHOUSE'])
api_router.include_router(mail.router, prefix="/mail", tags=['MAIL'])
api_router.include_router(product.router, prefix="/product", tags=['PRODUCT'])
api_router.include_router(image.router, prefix="/image", tags=['IMAGE'])
api_router.include_router(cart.router, prefix="/cart", tags=['CART'])
api_router.include_router(checkout.router, prefix="/checkout", tags=['CHECKOUT'])
api_router.include_router(payment.router, prefix="/payment", tags=['PAYMENT'])
api_router.include_router(paymentType.router, prefix="/payment/type", tags=['PAYMENT TYPE'])
api_router.include_router(order.router, prefix="/order", tags=['ORDER'])
