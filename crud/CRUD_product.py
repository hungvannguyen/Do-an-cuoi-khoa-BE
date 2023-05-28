from datetime import datetime
from typing import Any

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

    def get_all_products(self, db: Session):
        data_db = db.query(self.model).filter(
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        return data_db

    def get_all_active_products(self, db: Session):
        data_db = db.query(self.model).filter(
            self.model.status == 1,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        return data_db

    def get_product_by_id(self, id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.id == id,
            self.model.status == 1,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tồn tại Sản phẩm ID #{id}")
        return data_db

    def create_product(self, request, db: Session, admin_id):

        request = request.dict()
        cat_id = request['cat_id']
        if crud_category.get_category_by_id(db=db, id=cat_id):
            data_db = self.model(**request, insert_id=admin_id, update_id=admin_id)
            db.add(data_db)
            db.commit()
            db.refresh(data_db)
        return {
            'detail': "Tạo thành công"
        }

    def update_product(self, id, request, db: Session, admin_id):
        data_db = self.get_product_by_id(id, db=db)
        self.update(db_obj=data_db, obj_in=request, db=db, admin_id=admin_id)

        return {
            'detail': 'Cập nhật thành công'
        }


crud_product = CRUDProduct(Product)
