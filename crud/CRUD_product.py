from datetime import datetime
from typing import Any

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from crud.CRUD_category import crud_category
from models.product import Product
from schemas.product import *
from crud.base import CRUDBase
from constants import Const
from security.security import hash_password, verify_password, gen_token


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):

    def get_all_products(self, page: int, condition, db: Session):
        current_page = page
        if current_page <= 0:
            current_page = 1
        total_product = db.query(self.model).filter(
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        total_page = int(total_product / Const.ROW_PER_PAGE)
        if total_product % Const.ROW_PER_PAGE > 0:
            total_page += 1
        if current_page > total_page:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE
        limit = Const.ROW_PER_PAGE

        data_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if condition['sort'] == 1:
            data_db = data_db.order_by(asc(self.model.price))
        elif condition['sort'] == 2:
            data_db = data_db.order_by(desc(self.model.price))
        elif condition['sort'] == 3:
            data_db = data_db.filter(
                self.model.price >= condition['min_price'],
                self.model.price <= condition['max_price']
            )
        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")
        for item in data_db:
            if item.is_sale == 1:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)

        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def get_all_active_products(self, page: int, condition, db: Session):
        current_page = page
        if current_page <= 0:
            current_page = 1
        total_product = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        total_page = int(total_product / Const.ROW_PER_PAGE)
        if total_product % Const.ROW_PER_PAGE > 0:
            total_page += 1
        if current_page > total_page:
            current_page = total_page

        offset = (current_page - 1) * Const.ROW_PER_PAGE
        limit = Const.ROW_PER_PAGE
        data_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if condition['sort'] == 1:
            data_db = data_db.order_by(asc(self.model.price))
        elif condition['sort'] == 2:
            data_db = data_db.order_by(desc(self.model.price))
        elif condition['sort'] == 3:
            data_db = data_db.filter(
                self.model.price >= condition['min_price'],
                self.model.price <= condition['max_price']
            )
        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")
        for item in data_db:
            if item.is_sale == 1:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)

        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def get_product_by_id(self, id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.id == id,
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:
            return None
        if data_db.is_sale == 1:
            setattr(data_db, 'sale_price', data_db.price * (100 - data_db.sale_percent) / 100)
        else:
            setattr(data_db, 'sale_price', data_db.price)
        return data_db

    def get_sale_products(self, page: int, condition, db: Session):
        current_page = page
        if current_page <= 0:
            current_page = 1
        total_product = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        total_page = int(total_product / Const.ROW_PER_PAGE)
        if total_product % Const.ROW_PER_PAGE > 0:
            total_page += 1
        if current_page > total_page:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE
        limit = Const.ROW_PER_PAGE
        data_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.is_sale == Const.IS_SALE,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if condition['sort'] == 1:
            data_db = data_db.order_by(asc(self.model.price))
        elif condition['sort'] == 2:
            data_db = data_db.order_by(desc(self.model.price))
        elif condition['sort'] == 3:
            data_db = data_db.filter(
                self.model.price >= condition['min_price'],
                self.model.price <= condition['max_price']
            )
        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")
        for item in data_db:
            if item.is_sale == 1:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)

        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def get_new_products(self, page: int, db: Session):
        current_page = page
        if current_page <= 0:
            current_page = 1
        total_product = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        total_page = int(total_product / Const.ROW_PER_PAGE)
        if total_product % Const.ROW_PER_PAGE > 0:
            total_page += 1
        if current_page > total_page:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE
        limit = Const.ROW_PER_PAGE
        data_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")
        for item in data_db:
            if item.is_sale == 1:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)
        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def get_by_cat_id(self, cat_id, page, condition, db: Session):
        current_page = page
        if current_page <= 0:
            current_page = 1
        total_product = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        total_page = int(total_product / Const.ROW_PER_PAGE)
        if total_product % Const.ROW_PER_PAGE > 0:
            total_page += 1
        if current_page > total_page:
            current_page = total_page
        offset = (current_page - 1) * Const.ROW_PER_PAGE
        limit = Const.ROW_PER_PAGE
        data_db = db.query(self.model).filter(
            self.model.status == Const.ACTIVE_STATUS,
            self.model.cat_id == cat_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if condition['sort'] == 1:
            data_db = data_db.order_by(asc(self.model.price))
        elif condition['sort'] == 2:
            data_db = data_db.order_by(desc(self.model.price))
        elif condition['sort'] == 3:
            data_db = data_db.filter(
                self.model.price >= condition['min_price'],
                self.model.price <= condition['max_price']
            )
        data_db = data_db.order_by(self.model.insert_at.desc()).offset(offset).limit(limit).all()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy sản phẩm phù hợp")
        for item in data_db:
            if item.is_sale == 1:
                setattr(item, 'sale_price', item.price * (100 - item.sale_percent) / 100)
        return {
            'data': data_db,
            'current_page': current_page,
            'total_page': total_page
        }

    def create_product(self, request, db: Session, admin_id):

        request = request.dict()
        cat_id = request['cat_id']
        if request['is_sale'] == 0:
            request['sale_percent'] = 0
        if crud_category.get_category_by_id(db=db, id=cat_id):
            data_db = self.model(**request, insert_id=admin_id, update_id=admin_id, insert_at=datetime.utcnow(),
                                 update_at=datetime.utcnow())
            db.add(data_db)
            db.commit()
            db.refresh(data_db)
        return {
            'detail': "Tạo thành công"
        }

    def update_product(self, id, request, db: Session, admin_id):
        data_db = self.get_product_by_id(id, db=db)
        if not isinstance(request, dict):
            request = request.dict()
        if request['is_sale'] == 0:
            request['sale_percent'] = 0
        self.update(db_obj=data_db, obj_in=request, db=db, admin_id=admin_id)

        return {
            'detail': 'Cập nhật thành công'
        }


crud_product = CRUDProduct(Product)
