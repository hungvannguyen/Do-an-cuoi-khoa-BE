from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import models
import schemas.user
from models.user import User
from schemas.user import UserRegis, UserInfo
from crud.base import CRUDBase
from constants import Const
from security.security import hash_password, verify_password, gen_token


class CRUDUser(CRUDBase[User, UserRegis, UserInfo]):

    def get_user_by_id(self, db: Session, id):
        data_db = db.query(self.model).filter(
            self.model.id == id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        return data_db

    def get_user_by_account(self, db: Session, account):
        data_db = db.query(self.model).filter(
            User.account == account,
            User.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        return data_db

    def get_user_info(self, db: Session, id):
        data_db = self.get_user_by_id(db, id)
        data_db = jsonable_encoder(data_db)
        return data_db

    def login(self, db: Session, account, password):
        data_db = db.query(self.model).filter(
            User.account == account,
            User.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if data_db:
            data_db = jsonable_encoder(data_db)
            if verify_password(password, data_db['password']):
                return gen_token(data_db), data_db['role_id']
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Tài khoản hoặc mật khẩu không chính xác")

    def create_user(self, db: Session, request) -> Any:
        if not request.password == request.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Mật khẩu không khớp")
        data_db = db.query(self.model).filter(
            self.model.account == request.account,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if data_db.count():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài khoản này đã tồn tại")
        else:
            request = request.dict()
            password = request['password']
            hashed_password = hash_password(password)
            request['password'] = hashed_password
            data_db = self.model(account = request['account'], password = request['password'])
            db.add(data_db)
            db.commit()
            db.refresh(data_db)
            return {"result": "Tạo thành công"}

    def create_admin(self, db: Session, request, role_id) -> Any:
        request = request.dict()
        password = request['password']
        hashed_password = hash_password(password)
        request['password'] = hashed_password
        data_db = self.model(**request, role_id=role_id)
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        return {"result": "Tạo thành công"}

    def reset_password(self, db: Session, account_id, admin_id) -> Any:
        data_db = db.query(self.model).filter(
            self.model.id == account_id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if not data_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Không tìm thấy ID #{account_id}')
        data_db.update_at = datetime.utcnow()
        data_db.update_id = admin_id
        new_password = hash_password("user123")
        data_db.password = new_password
        db.add(data_db)
        db.commit()
        db.refresh(data_db)
        return {
            'detail': 'Đặt lại thành công'
        }

    def update_password(self, id, new_password, db: Session):
        user_db = self.get_user_by_id(db=db, id=id)
        new_hashed_password = hash_password(new_password)
        user_db.password = new_hashed_password
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        return {
            'detail': "Đã cập nhật mật khẩu"
        }


crud_user = CRUDUser(User)
