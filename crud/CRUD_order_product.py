from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import models
import schemas.user
from crud.base import CRUDBase
from models.order_product import Order_Product
from schemas.order_product import *
from constants import Const
from security.security import hash_password, verify_password, gen_token


class CRUDOrderProduct(CRUDBase[Order_Product, OrderProductCreate, OrderProductUpdate]):

    def get_by_order_id(self, order_id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.order_id == order_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        return data_db

    def create_order_product(self, request, db: Session, user_id):
        order_id = request['order_id']
        prd_id = request['prd_id']
        price = request['price']
        quantity = request['quantity']
        obj_db = self.model(ord_id=order_id, prd_id=prd_id, price=price, quantity=quantity, insert_id=user_id,
                            insert_at=datetime.utcnow(), update_id=user_id, update_at=datetime.utcnow())
        db.add(obj_db)
        db.commit()
        db.refresh(obj_db)

        return {
            'data': 'success'
        }

    def delete_order_product(self, order_product_id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.id == order_product_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        data_db.delete_flag = Const.DELETE_FLAG_DELETED
        db.add(data_db)
        db.commit()
        db.refresh(data_db)

        return {
            'detail': 'success'
        }


crud_order_product = CRUDOrderProduct(Order_Product)
