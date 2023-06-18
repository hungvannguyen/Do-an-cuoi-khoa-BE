from datetime import datetime
from typing import Any
from crud import logger
from constants import Method, Target
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
        logger.log(Method.GET, Target.ORDER_PRODUCT, comment=f"GET ALL ORDER_PRODUCT BY ORDER ID #{order_id}",
                   status=Target.SUCCESS,
                   id=0,
                   db=db)
        return data_db

    def create_order_product(self, request, db: Session, user_id):
        order_id = request['order_id']
        prd_id = request['prd_id']
        price = request['price']
        quantity = request['quantity']
        obj_db = self.model(ord_id=order_id, prd_id=prd_id, price=price, quantity=quantity, insert_id=user_id,
                            insert_at=datetime.now(), update_id=user_id, update_at=datetime.now())
        db.add(obj_db)
        db.commit()
        db.refresh(obj_db)
        logger.log(Method.POST, Target.ORDER_PRODUCT, comment=f"CREATE ORDER_PRODUCT IN ORDER ID #{order_id}",
                   status=Target.SUCCESS,
                   id=user_id,
                   db=db)
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
        logger.log(Method.DELETE, Target.ORDER_PRODUCT, comment=f"DELETE ORDER_PRODUCT ID #{order_product_id}",
                   status=Target.SUCCESS,
                   id=0,
                   db=db)
        return {
            'detail': 'success'
        }


crud_order_product = CRUDOrderProduct(Order_Product)
