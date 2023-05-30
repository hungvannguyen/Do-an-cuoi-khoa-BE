from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import models
import schemas.user
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate
from crud.CRUD_cart import crud_cart
from constants import Const
from security.security import hash_password, verify_password, gen_token


def get_checkout_info(db: Session, user_id):
    carts = crud_cart.get_cart(user_id=user_id, db=db)
    checkout = []
    total = 0
    if carts:
        for item in carts['products']:
            tmp = {
                'prd_id': item['prd_id'],
                'name': item['name'],
                'quantity': item['quantity'],
                'is_sale': item['is_sale'],
                'price': item['price'],
                'sale_price': item['sale_price']
            }
            total += item['sale_price'] * item['quantity']
            checkout.append(tmp)
    return {
        'products': checkout,
        'total': total
    }
