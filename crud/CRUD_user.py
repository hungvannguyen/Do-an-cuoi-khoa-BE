from typing import Any

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import models
import schemas.user
from models.user import User
from schemas import user
from crud.base import CRUDBase
from constants import Const


class CRUDUser(CRUDBase[User, schemas.user.UserRegis, schemas.user.UserInfo]):

    def get_user(self, db: Session, id):
        data_db = db.query(User).filter(
            self.model.id == id,
            self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        return data_db

    def get_user_by_account(self, db: Session, account):
        data_db = db.query(User).filter(
            User.account == account,
            User.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first()
        return data_db

    def create_user(self, db: Session, request) -> Any:
        if db.query(User).filter(
                self.model.account == request.account,
                self.model.delete_flag == Const.DELETE_FLAG_NORMAL
        ).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account exist")
        else:
            request = request.dict()
            data_db = self.model(**request)
            db.add(data_db)
            db.commit()
            db.refresh(data_db)
            return {"result": "Success"}


CRUD_user = CRUDUser(User)
