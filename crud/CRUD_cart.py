import json
from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from models import product
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
        total = 0
        if data_db:
            for item in data_db:
                prd_id = item.prd_id
                prd_data = jsonable_encoder(crud_product.get_product_by_id(id=prd_id, db=db))
                if not prd_data:
                    self.delete_cart(prd_id=prd_id, db=db, user_id=user_id)
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Reloading...")
                if item.quantity > prd_data['quantity']:
                    self.update_cart(prd_id=prd_id, quantity=prd_data['quantity'], db=db, user_id=user_id)
                data = jsonable_encoder(item)
                data['is_sale'] = prd_data['is_sale']
                if prd_data['is_sale'] == 1:
                    total += prd_data['price'] * data['quantity'] * (100 - prd_data['sale_percent']) / 100
                    data['sale_price'] = prd_data['sale_price']
                else:
                    data['sale_price'] = prd_data['sale_price']
                    total += prd_data['price'] * data['quantity']
                data['total_price'] = prd_data['sale_price'] * data['quantity']
                data['name'] = prd_data['name']
                data['price'] = prd_data['price']
                data['img_url'] = prd_data['img_url']
                result.append(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Giỏ hàng trống")

        return {
            'products': result,
            'total_price': total
        }

    def count_cart(self, db: Session, user_id):
        count = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        return count

    def add_to_cart(self, request, db: Session, user_id):
        prd_data = crud_product.get_product_by_id(id=request.prd_id, db=db)
        if not prd_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Không có sản phẩm ID #{request.prd_id}")
        data_db = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.prd_id == request.prd_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:
            request = request.dict()
            if request['quantity'] > prd_data.quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Sản phẩm đạt giới hạn")
            data_db = self.model(**request, insert_id=user_id, update_id=user_id, user_id=user_id)
            db.add(data_db)
            db.commit()
            db.refresh(data_db)
        else:
            if data_db.quantity + request.quantity > prd_data.quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Sản phẩm đạt giới hạn")
            self.update_cart(data_db.prd_id, request.quantity + data_db.quantity, db, user_id)
        return {
            'detail': "Đã thêm vào giỏ hàng"
        }

    def update_cart(self, prd_id, quantity, db: Session, user_id):
        data_db = db.query(self.model).filter(
            self.model.prd_id == prd_id,
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        prd_data = crud_product.get_product_by_id(id=prd_id, db=db)

        if prd_data.quantity < quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Sản phẩm đạt giới hạn")
        if data_db:
            data_db.update_id = user_id
            data_db.update_at = datetime.utcnow()
            data_db.quantity = quantity
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Không tìm thấy sản phẩm này trong giỏ hàng")
        data_db.delete_flag = Const.DELETE_FLAG_DELETED
        data_db.delete_at = datetime.utcnow()
        data_db.delete_id = user_id
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        return {
            'detail': "Đã xoá sản phẩm trong giỏ hàng"
        }

    def delete_all_cart(self, db: Session, user_id):
        data_db = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()

        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Giỏ hàng trống")

        for item in data_db:
            self.delete_cart(prd_id=item.prd_id, db=db, user_id=user_id)

        return {
            'detail': "Đã xoá toàn bộ giỏ hàng"
        }

    def check_cart_to_order(self, db: Session, user_id):
        data_db = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if data_db:
            for item in data_db:
                prd_id = item.prd_id
                prd_data = db.query(product.Product).filter(
                    product.Product.id == prd_id,
                    product.Product.delete_flag == Const.DELETE_FLAG_NORMAL
                ).first()
                if item.quantity > prd_data.quantity:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="Số lượng sản phẩm quá lớn")
        return {
            'detail': 'success'
        }


crud_cart = CRUDCart(Cart)
