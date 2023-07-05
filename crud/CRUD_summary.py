import json
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from crud import logger
from constants import Method, Target
from models import product
from models.order import Order
from schemas.cart import *
from crud.base import CRUDBase
from crud.CRUD_order import crud_product, crud_order_product
from constants import Const


def total_income(db: Session):
    total_income = 0
    total_profit = 0
    count = 0
    order_db = db.query(Order).filter(
        Order.status == Const.ORDER_SUCCESS,
        Order.delete_flag == Const.DELETE_FLAG_NORMAL
    ).all()

    for item in order_db:
        count += 1
        order_product_db = crud_order_product.get_by_order_id(order_id=item.id, db=db)
        for item2 in order_product_db:
            total_income += item2.price * item2.quantity
            total_profit += (item2.price - item2.import_price) * item2.quantity

    return {
        'total_income': total_income,
        'total_profit': total_profit,
        'order_count': count
    }