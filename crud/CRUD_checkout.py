from datetime import datetime
from typing import Any
from crud import logger
from constants import Method, Target
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import models
import schemas.user
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate
from crud.CRUD_cart import crud_cart
from crud.CRUD_user import crud_user
from crud.CRUD_address import crud_address
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


def get_checkout_user_info(db: Session, user_id):
    # user_info = crud_user.get_user_info(db, user_id)
    result = {
        # 'name': user_info['name'],
        # 'email': user_info['email'],
        # 'phone_number': user_info['phone_number'],
        'address': None
    }
    address_info = crud_address.get_address_info_by_user_id(user_id=user_id, db=db)
    if address_info:
        result['address'] = address_info
    return result


