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

    def get_user(self, db: Session, id):
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

    def login(self, db: Session, account, password):
        data_db = db.query(self.model).filter(
            User.account == account,
            User.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        if data_db:
            data_db = jsonable_encoder(data_db)
            if verify_password(password, data_db['password']):
                return gen_token(data_db)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account or password incorrect")

    def create_user(self, db: Session, request) -> Any:
        data_db = db.query(self.model).filter(
                self.model.account == request.account,
                self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        )
        if data_db.count():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account exist")
        else:
            request = request.dict()
            password = request['password']
            hashed_password = hash_password(password)
            request['password'] = hashed_password
            print(request)
            data_db = self.model(**request)
            db.add(data_db)
            db.commit()
            db.refresh(data_db)
            return {"result": "Success"}


crud_user = CRUDUser(User)
