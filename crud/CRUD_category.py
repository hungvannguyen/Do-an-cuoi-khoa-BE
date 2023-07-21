import json
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
from models.product import Product
from schemas.category import CategoryCreate, CategoryUpdate
from crud.base import CRUDBase
from constants import Const
from security.security import hash_password, verify_password, gen_token


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):

    def get_category_by_id(self, id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.id == id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        if not data_db:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Không tìm thấy danh mục ID #{id}")

        data_db = db.query(self.model).filter(
            self.model.id == id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        return data_db

    def get_all_category(self, db: Session):
        data_db = db.query(self.model).filter(
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tồn tại Danh mục nào")

        data_db = db.query(self.model).filter(
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).all()
        return data_db

    def create_category(self, request, admin_id, db: Session):
        cat_name = str(request.cat_name)
        data_db = db.query(self.model).filter(
            self.model.cat_name == cat_name,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if data_db:

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Danh mục đã tồn tại")

        request = request.dict()
        data_db = self.model(**request, insert_id=admin_id, update_id=admin_id)
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        logger.log(Method.POST, Target.CATEGORY, comment=f"CREATE NEW CATEGORY {cat_name}",
                   status=Target.SUCCESS,
                   id=admin_id,
                   db=db)
        return {
            'detail': "Tạo thành công"
        }

    def update_category(self, request, id, db: Session, admin_id):
        if not isinstance(request, dict):
            request = request.dict()
        data_db = self.get_category_by_id(id, db)
        self.update(db_obj=data_db, obj_in=request, db=db, admin_id=admin_id)
        logger.log(Method.PUT, Target.CATEGORY, comment=f"UPDATE CATEGORY ID {id}",
                   status=Target.SUCCESS,
                   id=admin_id,
                   db=db)
        return {
            'detail': "Cập nhật thành công"
        }

    def delete_category(self, id: int, db: Session, admin_id):

        prd_count = db.query(Product).filter(
            Product.cat_id == id,
            Product.delete_flag == Const.DELETE_FLAG_NORMAL
        ).count()

        if prd_count > 0:

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Không thể xóa vì có sản phẩm ở danh mục này đang bán")

        data_db = self.get_category_by_id(id, db)
        cat_name = data_db.cat_name
        self.delete(db=db, db_obj=data_db, admin_id=admin_id)
        logger.log(Method.DELETE, Target.CATEGORY, comment=f"DELETE CATEGORY {cat_name}",
                   status=Target.SUCCESS,
                   id=admin_id,
                   db=db)
        return {
            'detail': "Đã xoá"
        }


crud_category = CRUDCategory(Category)
