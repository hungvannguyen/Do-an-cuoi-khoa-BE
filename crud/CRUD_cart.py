import json
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from models.cart import Cart
from schemas.cart import *
from crud.base import CRUDBase
from crud.CRUD_product import crud_product
from constants import Const


class CRUDCart(CRUDBase[Cart, CartCreate, CartUpdate]):

    def get_cart(self, user_id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.quantity > 0,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        result = []
        if data_db:
            for item in data_db:
                data = jsonable_encoder(item)
                prd_id = data['prd_id']
                prd_data = jsonable_encoder(crud_product.get_product_by_id(id=prd_id, db=db))
                data['name'] = prd_data['name']
                data['img_url'] = prd_data['img_url']
                result.append(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Giỏ hàng trống")

        return result

    def create_cart(self, request, db: Session, user_id):
        prd_data = crud_product.get_product_by_id(id=request.prd_id, db=db)
        if not prd_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không có sản phẩm ID #{request.prd_id}")
        data_db = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.prd_id == request.prd_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:
            request = request.dict()
            data_db = self.model(**request, insert_id=user_id, update_id=user_id, user_id = user_id)
            db.add(data_db)
            db.commit()
            db.refresh(data_db)
        else:
            self.update_cart(data_db.prd_id, request.quantity, db, user_id)
        return {
            'detail': "Đã thêm vào giỏ hàng"
        }

    def update_cart(self, prd_id, quantity, db: Session, user_id):
        data_db = db.query(self.model).filter(
            self.model.prd_id == prd_id,
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if data_db:
            data_db.update_id = user_id
            data_db.update_at = datetime.utcnow()
            if quantity == 0:
                data_db.quantity = 0
                data_db.delete_flag = Const.DELETE_FLAG_DELETED
                data_db.delete_id = user_id
                data_db.delete_at = datetime.utcnow()
                db.add(data_db)
                db.commit()
                db.refresh(data_db)
            else:
                data_db.quantity += quantity
                db.add(data_db)
                db.commit()
                db.refresh(data_db)
        return {
            'detail': "Đã cập nhật giỏ hàng"
        }

    def delete_cart(self, prd_id, db: Session, user_id):
        data_db = db.query(self.model).filter(
            self.model.prd_id == prd_id,
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Không tìm thấy sản phẩm này trong giỏ hàng")
        data_db.delete_flag = Const.DELETE_FLAG_DELETED
        data_db.delete_at = datetime.utcnow()
        data_db.delete_id = user_id
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        return {
            'detail': "Đã xoá sản phẩm trong giỏ hàng"
        }


crud_cart = CRUDCart(Cart)
