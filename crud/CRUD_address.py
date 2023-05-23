from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from models.address import Address
from schemas.address import AddressInfo, AddressCreate, AddressUpdate
from crud.base import CRUDBase
from constants import Const
from security.security import hash_password, verify_password


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):
    def get_address_by_user_id(self, user_id, db: Session):
        data_db = db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()

        return data_db

    def create_address(self, request, db: Session, user_id):
        data_db = self.get_address_by_user_id(user_id=user_id, db=db)
        if data_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"User ID #{request.user_id} đã có Đị̣a chỉ")
        request = request.dict()
        data_db = self.model(**request, insert_id=user_id, update_id=user_id, user_id = user_id)
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        return {
            'detail': "Đã tạo Địa chỉ thành công"
        }

    def update_address(self, request, db: Session, user_id):
        data_db = self.get_address_by_user_id(user_id=user_id, db=db)
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User ID #{user_id} chưa có Địa chỉ nào")
        self.update(db=db, obj_in=request, db_obj=data_db, admin_id=user_id)
        return {
            'detail': "Cập nhật thành công"
        }

    def delete_address(self, user_id, db: Session, admin_id):
        data_db = self.get_address_by_user_id(user_id, db)
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User ID #{user_id} chưa có Địa chỉ nào")
        self.delete(db=db, db_obj=data_db, admin_id=admin_id)
        return {
            'detail': "Đã xoá"
        }


crud_address = CRUDAddress(Address)
